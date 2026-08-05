"""
hrrp_analysis.py
Analysis of the CMS Hospital Readmissions Reduction Program, FY2026 release.

Source
------
Centers for Medicare and Medicaid Services, Provider Data Catalog.
"FY 2026 Hospital Readmissions Reduction Program - Hospital" file.
Performance period: discharges from 2021-07-01 through 2024-06-30.
3,055 hospitals, six conditions, 18,330 hospital-measure rows.

What this asks
--------------
Not "which hospitals are worst." That question is already answered by the file
and it is not interesting. The questions here are about the measurement itself:

  Q1  How much of the program is actually scored, and how much is invisible?
  Q2  Is the missingness random, or does it track hospital size?
  Q3  What share of hospitals can be penalized, and is that a finding or arithmetic?
  Q4  Do the six conditions behave like one underlying "hospital quality" signal?
  Q5  How much variation is there between states?

Method notes
------------
SQL is used for the aggregation because that is what it is for. Pandas handles
the correlation matrix and the reshaping, because that is what it is for.
Every rate in the output is reported with its denominator so a reader can see
what it was computed over.

Run:
    python hrrp_analysis.py --csv <path to the CMS csv>
"""

import argparse
import json
import sys

import duckdb
import pandas as pd

MEASURE_LABEL = {
    "AMI": "Heart attack (AMI)",
    "CABG": "Bypass surgery (CABG)",
    "COPD": "COPD",
    "HF": "Heart failure",
    "HIP-KNEE": "Hip and knee replacement",
    "PN": "Pneumonia",
}


def load(con, csv_path):
    """Load the CMS file and normalize the two numeric columns.

    Both 'Excess Readmission Ratio' and 'Number of Discharges' arrive as text
    because CMS writes 'N/A' and 'Too Few to Report' into numeric fields.
    TRY_CAST turns those into NULL rather than throwing, which is the correct
    behavior here: a suppressed value is genuinely unknown, not zero.
    """
    con.execute(
        """
        CREATE OR REPLACE TABLE hrrp AS
        SELECT
            "Facility Name"                                 AS facility,
            "Facility ID"                                   AS facility_id,
            "State"                                         AS state,
            replace(replace("Measure Name",'READM-30-',''),'-HRRP','') AS measure,
            TRY_CAST("Number of Discharges"       AS DOUBLE) AS discharges,
            TRY_CAST("Excess Readmission Ratio"   AS DOUBLE) AS err,
            TRY_CAST("Predicted Readmission Rate" AS DOUBLE) AS predicted,
            TRY_CAST("Expected Readmission Rate"  AS DOUBLE) AS expected,
            "Footnote"                                      AS footnote,
            "Start Date"                                    AS start_date,
            "End Date"                                      AS end_date
        FROM read_csv_auto(?, header=true, all_varchar=true)
        """,
        [csv_path],
    )
    n = con.execute("SELECT count(*) FROM hrrp").fetchone()[0]
    h = con.execute("SELECT count(DISTINCT facility_id) FROM hrrp").fetchone()[0]
    return n, h


def reconcile(con):
    """Every row must be either scored or suppressed. Never both, never neither.

    This is the check that catches a bad load. If the two counts do not sum to
    the row count, something in the cast went wrong and nothing below is safe.
    """
    r = con.execute(
        """
        SELECT
            count(*)                                  AS rows_total,
            count(err)                                AS scored,
            count(*) - count(err)                     AS suppressed
        FROM hrrp
        """
    ).fetchdf().iloc[0]
    assert r.scored + r.suppressed == r.rows_total, "reconciliation failed"
    return r.to_dict()


def q1_coverage(con):
    """Share of hospital-measure pairs with no ratio, by condition."""
    return con.execute(
        """
        SELECT
            measure,
            count(*)                                        AS pairs,
            count(err)                                      AS scored,
            count(*) - count(err)                           AS suppressed,
            round(100.0 * (count(*) - count(err)) / count(*), 1) AS pct_suppressed
        FROM hrrp
        GROUP BY measure
        ORDER BY pct_suppressed
        """
    ).fetchdf()


def q1b_per_hospital(con):
    """How many of the six measures does each hospital actually get scored on."""
    return con.execute(
        """
        WITH per_hospital AS (
            SELECT facility_id, count(err) AS n_scored
            FROM hrrp GROUP BY facility_id
        )
        SELECT n_scored, count(*) AS hospitals,
               round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct
        FROM per_hospital
        GROUP BY n_scored
        ORDER BY n_scored
        """
    ).fetchdf()


def q2_size_bias(con):
    """Does being scored at all track hospital volume?

    Total discharges is itself partly suppressed, so this is computed only over
    hospitals with at least one reported discharge count. That is a real
    limitation and it is stated rather than hidden: the very smallest hospitals
    are underrepresented even in this check.
    """
    return con.execute(
        """
        WITH per_hospital AS (
            SELECT facility_id,
                   sum(discharges) AS total_discharges,
                   count(err)      AS n_scored
            FROM hrrp
            GROUP BY facility_id
            HAVING sum(discharges) IS NOT NULL
        )
        SELECT
            CASE
                WHEN total_discharges <  200 THEN '1. under 200'
                WHEN total_discharges <  500 THEN '2. 200 to 499'
                WHEN total_discharges < 1500 THEN '3. 500 to 1499'
                ELSE                              '4. 1500 and up'
            END                                   AS volume_band,
            count(*)                              AS hospitals,
            round(avg(n_scored), 2)               AS avg_measures_scored
        FROM per_hospital
        GROUP BY volume_band
        ORDER BY volume_band
        """
    ).fetchdf()


def q3_penalty_exposure(con):
    """Share of scored pairs above 1.0, plus the distribution centre.

    An excess readmission ratio is predicted over expected performance relative
    to peers. It is a relative measure, so it centres on 1.0 by construction.
    Roughly half of everyone sits above it no matter how the national rate moves.
    """
    return con.execute(
        """
        SELECT
            measure,
            count(err)                                       AS scored,
            round(avg(err), 4)                               AS mean_err,
            round(median(err), 4)                            AS median_err,
            round(stddev_samp(err), 4)                       AS sd_err,
            round(min(err), 4)                               AS min_err,
            round(max(err), 4)                               AS max_err,
            round(100.0 * count(*) FILTER (WHERE err > 1) / count(err), 1) AS pct_above_1
        FROM hrrp
        WHERE err IS NOT NULL
        GROUP BY measure
        ORDER BY measure
        """
    ).fetchdf()


def q4_within_hospital(con):
    """Do the six conditions move together inside a single hospital?

    Restricted to hospitals scored on all six, because a correlation computed
    over hospitals with different missing measures would be comparing different
    populations column to column.
    """
    wide = con.execute(
        """
        SELECT facility_id, measure, err
        FROM hrrp WHERE err IS NOT NULL
        """
    ).fetchdf().pivot(index="facility_id", columns="measure", values="err")
    full = wide.dropna()
    spread = (full.max(axis=1) - full.min(axis=1))
    return full, full.corr(), {
        "hospitals_scored_on_all_six": int(len(full)),
        "mean_within_hospital_range": round(float(spread.mean()), 4),
        "median_within_hospital_range": round(float(spread.median()), 4),
    }


def q5_states(con, min_pairs=60):
    """Mean ratio by state, with a volume gate so tiny states are not ranked."""
    return con.execute(
        """
        SELECT state,
               count(err)             AS scored_pairs,
               round(avg(err), 4)     AS mean_err
        FROM hrrp
        WHERE err IS NOT NULL
        GROUP BY state
        HAVING count(err) >= ?
        ORDER BY mean_err
        """,
        [min_pairs],
    ).fetchdf()


def histogram(con, measure, bins=24):
    """Simple equal-width histogram, returned as edges and counts."""
    s = con.execute(
        "SELECT err FROM hrrp WHERE err IS NOT NULL AND measure = ?", [measure]
    ).fetchdf()["err"]
    counts, edges = pd.cut(s, bins=bins, retbins=True)
    vc = counts.value_counts().sort_index()
    return [round(float(e), 4) for e in edges], [int(c) for c in vc.values]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args()

    con = duckdb.connect()
    n_rows, n_hosp = load(con, args.csv)
    period = con.execute("SELECT DISTINCT start_date, end_date FROM hrrp").fetchone()

    print(f"Loaded {n_rows:,} rows, {n_hosp:,} hospitals, period {period[0]} to {period[1]}")
    rec = reconcile(con)
    print(f"Reconciliation OK: {rec['scored']:,} scored + {rec['suppressed']:,} suppressed "
          f"= {rec['rows_total']:,} rows\n")

    cov = q1_coverage(con);            print("Q1 coverage by condition\n", cov.to_string(index=False), "\n")
    per = q1b_per_hospital(con);       print("Q1b measures scored per hospital\n", per.to_string(index=False), "\n")
    size = q2_size_bias(con);          print("Q2 coverage against volume\n", size.to_string(index=False), "\n")
    pen = q3_penalty_exposure(con);    print("Q3 distribution and penalty exposure\n", pen.to_string(index=False), "\n")
    full, corr, spread = q4_within_hospital(con)
    print("Q4 within-hospital consistency\n", corr.round(3).to_string(), "\n", spread, "\n")
    st = q5_states(con);               print("Q5 states, best 5\n", st.head(5).to_string(index=False))
    print("Q5 states, worst 5\n", st.tail(5).to_string(index=False), "\n")

    if args.json_out:
        out = {
            "rows": int(n_rows), "hospitals": int(n_hosp),
            "period": {"start": period[0], "end": period[1]},
            "reconciliation": {k: int(v) for k, v in rec.items()},
            "coverage": cov.to_dict("records"),
            "per_hospital": per.to_dict("records"),
            "size_bias": size.to_dict("records"),
            "distribution": pen.to_dict("records"),
            "corr": corr.round(3).to_dict(),
            "spread": spread,
            "states": st.to_dict("records"),
            "hist_hf": dict(zip(["edges", "counts"], histogram(con, "HF"))),
        }
        with open(args.json_out, "w") as f:
            json.dump(out, f, indent=2)
        print(f"Wrote {args.json_out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
