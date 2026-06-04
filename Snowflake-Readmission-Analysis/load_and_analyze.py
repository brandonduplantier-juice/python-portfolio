#!/usr/bin/env python3
"""Load the hospital readmission dataset into Snowflake and run analytics.

This is a CLOUD warehouse demo - it requires a Snowflake account (free trial).
Credentials are read from snowflake_config.json (never hardcoded, never commit it).
"""
import json
import os
import sys

import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

CFG = "snowflake_config.json"
if not os.path.exists(CFG):
    sys.exit(
        "Missing snowflake_config.json - copy snowflake_config.template.json to "
        "snowflake_config.json and fill in your account, user, and password."
    )
cfg = json.load(open(CFG))

DB, SCHEMA, TABLE = "READMISSIONS_DB", "ANALYTICS", "READMISSIONS"
WH = cfg.get("warehouse", "COMPUTE_WH")

conn = snowflake.connector.connect(
    account=cfg["account"],
    user=cfg["user"],
    password=cfg["password"],
    role=cfg.get("role", "ACCOUNTADMIN"),
)
cur = conn.cursor()


def exec_sql(sql):
    cur.execute(sql)


def query_df(sql):
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    return pd.DataFrame(cur.fetchall(), columns=cols)


# --- environment ---
exec_sql(
    f"CREATE WAREHOUSE IF NOT EXISTS {WH} WAREHOUSE_SIZE=XSMALL "
    f"AUTO_SUSPEND=60 AUTO_RESUME=TRUE INITIALLY_SUSPENDED=FALSE"
)
exec_sql(f"USE WAREHOUSE {WH}")
exec_sql(f"CREATE DATABASE IF NOT EXISTS {DB}")
exec_sql(f"USE DATABASE {DB}")
exec_sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
exec_sql(f"USE SCHEMA {SCHEMA}")

# --- table + load ---
df = pd.read_csv("hospital_readmissions.csv")
df.columns = [c.upper() for c in df.columns]
exec_sql(
    f"""CREATE OR REPLACE TABLE {TABLE} (
  PATIENT_ID STRING, AGE NUMBER, GENDER STRING, PRIMARY_DIAGNOSIS STRING,
  DEPARTMENT STRING, INSURANCE_TYPE STRING, LENGTH_OF_STAY_DAYS NUMBER,
  DISCHARGE_DISPOSITION STRING, FOLLOWUP_SCHEDULED STRING,
  RISK_SCORE_AT_DISCHARGE FLOAT, ADMISSION_DATE STRING, DISCHARGE_DATE STRING,
  READMITTED_30_DAYS STRING, DAYS_TO_READMISSION NUMBER)"""
)
ok, _, nrows, _ = write_pandas(conn, df, TABLE)
print(f"Loaded {nrows} rows into {DB}.{SCHEMA}.{TABLE}\n")

# --- analytics (Snowflake SQL: IFF, QUALIFY, RATIO_TO_REPORT, windows) ---
queries = {
    "rate_by_diagnosis": """
        SELECT PRIMARY_DIAGNOSIS,
               COUNT(*) AS PATIENTS,
               SUM(IFF(READMITTED_30_DAYS='Yes',1,0)) AS READMITTED,
               ROUND(AVG(IFF(READMITTED_30_DAYS='Yes',1,0))*100,2) AS READMIT_RATE_PCT
        FROM READMISSIONS
        GROUP BY PRIMARY_DIAGNOSIS
        ORDER BY READMIT_RATE_PCT DESC""",
    "highest_risk_diagnosis_qualify": """
        SELECT * FROM (
          SELECT PRIMARY_DIAGNOSIS,
                 ROUND(AVG(IFF(READMITTED_30_DAYS='Yes',1,0))*100,2) AS READMIT_RATE_PCT
          FROM READMISSIONS
          GROUP BY PRIMARY_DIAGNOSIS
        )
        QUALIFY ROW_NUMBER() OVER (ORDER BY READMIT_RATE_PCT DESC) = 1""",
    "insurance_share_of_readmits": """
        SELECT INSURANCE_TYPE,
               COUNT(*) AS PATIENTS,
               SUM(IFF(READMITTED_30_DAYS='Yes',1,0)) AS READMITTED,
               ROUND(RATIO_TO_REPORT(SUM(IFF(READMITTED_30_DAYS='Yes',1,0)))
                     OVER ()*100,1) AS PCT_OF_ALL_READMITS
        FROM READMISSIONS
        GROUP BY INSURANCE_TYPE
        ORDER BY READMITTED DESC""",
    "followup_effect": """
        SELECT FOLLOWUP_SCHEDULED,
               COUNT(*) AS PATIENTS,
               ROUND(AVG(IFF(READMITTED_30_DAYS='Yes',1,0))*100,2) AS READMIT_RATE_PCT
        FROM READMISSIONS
        GROUP BY FOLLOWUP_SCHEDULED
        ORDER BY READMIT_RATE_PCT DESC""",
}

for name, sql in queries.items():
    out = query_df(sql)
    print(f"===== {name} =====")
    print(out.to_string(index=False))
    print()
    out.to_csv(f"result_{name}.csv", index=False)

cur.close()
conn.close()
print("Done. Result CSVs written to the project folder.")
