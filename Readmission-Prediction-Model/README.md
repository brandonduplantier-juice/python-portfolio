\# Hospital Readmission Prediction Model



\## Overview

Logistic regression and Random Forest classifier predicting 30-day hospital

readmission using patient-level clinical features. Built on the same 300-patient

dataset used in the Power BI and Looker Studio dashboards, extending the analysis

from descriptive to predictive.



\## Business Question

Which patient features best predict 30-day readmission risk?



\## Model Performance

\- ROC-AUC: 0.587

\- Accuracy: 77%

\- Dataset: 300 patients, 24% readmission rate (class imbalance handled with

&#x20; class\_weight='balanced')



\## Key Findings

\- Risk\_Score\_at\_Discharge is the strongest predictor

\- Followup\_Scheduled is the strongest protective factor

\- Model correctly identifies high-risk patients while minimizing false negatives



\## Features Used

Age, Length of Stay, Risk Score at Discharge, Gender, Followup Scheduled,

Insurance Type, Primary Diagnosis, Discharge Disposition



\## Techniques

\- Random Forest Classifier (scikit-learn)

\- Class imbalance handling (class\_weight='balanced')

\- Train/test split with stratification

\- ROC-AUC evaluation

\- Confusion matrix visualization

\- Feature importance ranking



\## Files

\- `readmission\_model.py` - full model pipeline

\- `readmission\_model\_result

