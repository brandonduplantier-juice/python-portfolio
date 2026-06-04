# Hospital Readmission - Logistic Regression (R)

Interpretable logistic-regression companion to the Python Random Forest readmission
model, run on the same 300-patient dataset. Where the Random Forest predicts who is at
risk, this model quantifies *how much* each factor changes the odds of 30-day
readmission, reported as odds ratios with confidence intervals.

## Files
- `readmission_logistic_regression.R` - the analysis script
- `hospital_readmissions.csv` - the dataset (300 patients)
- `logistic_odds_ratios.csv` - generated on run: odds ratios, 95% CIs, p-values
- `roc_curve.png` - generated on run: ROC curve with AUC

## Method
Binomial logistic regression (`glm`, logit link) predicting `Readmitted_30_Days` from
age, primary diagnosis, insurance type, length of stay, discharge disposition, followup
scheduling, and risk score at discharge. Hip/Knee Replacement (the lowest-readmission
diagnosis) is the reference category, so diagnosis odds ratios read as risk relative to
it. Department is excluded to avoid collinearity with diagnosis; `Days_to_Readmission`
is excluded as a post-outcome leak. Discrimination is reported as ROC AUC.

## Run
Requires R (4.x) and the `pROC` package, which the script auto-installs on first run.

```
Rscript readmission_logistic_regression.R
```

Or open the script in RStudio and source it. Outputs are written to the working
directory. Run from inside the project folder so it finds `hospital_readmissions.csv`.
