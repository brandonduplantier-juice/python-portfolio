# Hospital Readmission - Excel Analysis

The spreadsheet version of the 300-patient hospital readmission analysis, part of a
multi-tool series that runs the same question across R, SQL, Power BI, Snowflake, and
Excel to show the result does not depend on the tool.

## What it is
A single Excel workbook that takes the raw readmission data and works it up into a
summary and a dashboard using native spreadsheet features, no code. It demonstrates
that the readmission patterns (which diagnoses and factors drive 30-day readmission)
are reproducible with ordinary office tools, which matters because many stakeholders
live in Excel.

## The workbook
`hospital_readmissions_excel.xlsx`, with four sheets:

- **Raw Data** - the 300-patient dataset as imported.
- **Summary Tables** - pivot-table breakdowns of readmission rate by diagnosis,
  insurance type, and other factors.
- **Formulas** - the worked calculations behind the summaries (rates, counts,
  conditional aggregations), shown rather than hidden.
- **Dashboard** - the headline charts and figures pulled together on one sheet.

## How to view
Open the .xlsx in Excel, Google Sheets, or LibreOffice Calc. Everything is
self-contained; there is nothing to run or install.

## Companion versions
For the interpretable statistical version of the same analysis (odds ratios with
confidence intervals and ROC AUC), see the `R-Readmission-Logistic-Regression` folder
in this repository.
