# Hospital 30-Day Readmission Analysis

## Overview
Interactive Power BI dashboard analyzing 30-day readmission rates across 
300 patients using a synthetic hospital dataset modeled on CMS HRRP metrics.

## Business Question
Which patient populations are being readmitted within 30 days, and what 
operational factors are driving it

## Key Findings
- Overall 30-day readmission rate 24%
- Heart Failure highest readmission rate at 39%
- HipKnee Replacement lowest at 7%
- Patients discharged home showed higher readmission rates than those 
  sent to skilled nursing facilities

## Tools
- Power BI Desktop
- DAX (COUNTROWS, FILTER, DIVIDE, AVERAGE)
- CSV dataset (300 patients, 14 variables)

## Dashboard Features
- 3 KPI cards Total Patients, Total Readmissions, Readmission Rate
- Bar chart Readmission rate by diagnosis
- Line chart Patient volume and readmissions by month
- Bar chart Readmission rate by discharge disposition
- Slicers Insurance Type, Department, Gender

## Files
- `hospital_readmissions.csv` — source dataset
- `readmissions_dashboard.pbix` — Power BI project file
- `readmissions_dashboard.pdf` — exported dashboard