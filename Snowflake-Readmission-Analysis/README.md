# Hospital Readmission - Snowflake Data Warehouse

Loads the 300-patient hospital readmission dataset into a Snowflake cloud data
warehouse and runs analytical SQL (readmission rates by diagnosis and insurance,
highest-risk diagnosis, followup effect) using Snowflake features: `IFF`, `QUALIFY`,
`RATIO_TO_REPORT`, and window functions.

## Important
Snowflake is a cloud warehouse, not a local install. You need a (free trial) Snowflake
account. This package installs only the Python client and loads/queries the data.

## Files
- `load_and_analyze.py` - connects, creates the DB/schema/table, loads the CSV, runs analytics
- `queries.sql` - the same analytics to run directly in the Snowsight web UI
- `hospital_readmissions.csv` - the dataset (300 patients)
- `snowflake_config.template.json` - credential template (copy to `snowflake_config.json`)
- `requirements.txt` - Python dependencies
- `result_*.csv` - generated on run

## Setup
1. Sign up for a free Snowflake trial at https://signup.snowflake.com
   Record: account identifier, username, password. The account identifier is in your
   Snowsight URL: `https://app.snowflake.com/<ORG>/<ACCOUNT>/` -> use `<ORG>-<ACCOUNT>`.
2. Copy `snowflake_config.template.json` to `snowflake_config.json` and fill in
   account, user, and password. Do NOT commit or share `snowflake_config.json`.
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python load_and_analyze.py`

Outputs print to the console and write `result_*.csv` files. The free-trial warehouse
is time-limited, so capture the console output / result CSVs as the portfolio artifact.

## Security note
`snowflake_config.json` holds your password in plaintext. Keep it local only. If this
project is ever pushed to GitHub, add `snowflake_config.json` to `.gitignore` first.
