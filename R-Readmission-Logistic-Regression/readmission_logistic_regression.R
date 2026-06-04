# Hospital 30-Day Readmission - Logistic Regression
# Interpretable companion to the Python Random Forest model.
# Same 300-patient dataset; this model quantifies how each factor
# changes the ODDS of 30-day readmission (odds ratios), where the
# Random Forest focused on prediction.
#
# Base R only - no external packages required.

# --- load ---
data_file <- "hospital_readmissions.csv"
df <- read.csv(data_file, stringsAsFactors = FALSE)

# --- prepare ---
df$Readmitted <- ifelse(df$Readmitted_30_Days == "Yes", 1L, 0L)
df$Primary_Diagnosis     <- factor(df$Primary_Diagnosis)
df$Insurance_Type        <- factor(df$Insurance_Type)
df$Discharge_Disposition <- factor(df$Discharge_Disposition)
df$Followup_Scheduled    <- factor(df$Followup_Scheduled, levels = c("No", "Yes"))

# Reference category = the lowest-readmission diagnosis, so odds ratios
# read as "risk relative to Hip/Knee Replacement".
df$Primary_Diagnosis <- relevel(df$Primary_Diagnosis, ref = "Hip/Knee Replacement")

# --- model ---
# Department excluded: collinear with diagnosis (each diagnosis maps to one
# department here). Days_to_Readmission excluded: post-outcome leak.
model <- glm(
  Readmitted ~ Age + Primary_Diagnosis + Insurance_Type +
    Length_of_Stay_Days + Discharge_Disposition +
    Followup_Scheduled + Risk_Score_at_Discharge,
  data = df,
  family = binomial(link = "logit")
)

cat("\n===== Model Summary =====\n")
print(summary(model))

# --- odds ratios + 95% CI (Wald) ---
ci <- exp(confint.default(model))
or_tab <- data.frame(
  Term       = names(coef(model)),
  Odds_Ratio = round(exp(coef(model)), 4),
  CI_Lower   = round(ci[, 1], 4),
  CI_Upper   = round(ci[, 2], 4),
  P_Value    = round(summary(model)$coefficients[, 4], 4),
  row.names  = NULL
)
cat("\n===== Odds Ratios (95% CI) =====\n")
print(or_tab, row.names = FALSE)
write.csv(or_tab, "logistic_odds_ratios.csv", row.names = FALSE)

# --- predicted probabilities ---
df$pred_prob <- predict(model, type = "response")

# --- AUC (Mann-Whitney, base R) ---
auc_fn <- function(y, p) {
  pos <- p[y == 1]
  neg <- p[y == 0]
  mean(sapply(pos, function(a) mean((a > neg) + 0.5 * (a == neg))))
}
auc_val <- auc_fn(df$Readmitted, df$pred_prob)
cat(sprintf("\nModel AUC: %.3f\n", auc_val))

# --- ROC curve (base R) ---
thr <- sort(unique(c(0, df$pred_prob, 1)), decreasing = TRUE)
npos <- sum(df$Readmitted == 1)
nneg <- sum(df$Readmitted == 0)
tpr <- sapply(thr, function(t) sum(df$pred_prob >= t & df$Readmitted == 1) / npos)
fpr <- sapply(thr, function(t) sum(df$pred_prob >= t & df$Readmitted == 0) / nneg)

png("roc_curve.png", width = 800, height = 600)
plot(fpr, tpr, type = "l", col = "#1a3a5c", lwd = 2,
     xlab = "False Positive Rate", ylab = "True Positive Rate",
     main = sprintf("Logistic Regression ROC (AUC = %.3f)", auc_val))
abline(0, 1, lty = 2, col = "gray60")
dev.off()

cat("\nSaved: logistic_odds_ratios.csv, roc_curve.png\n")
