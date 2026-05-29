import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, roc_curve, ConfusionMatrixDisplay)
import warnings
warnings.filterwarnings('ignore')

# 1. LOAD DATA
df = pd.read_csv('../Hospital-Readmission-PowerBI/hospital_readmissions.csv')
print(f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Readmission rate: {(df['Readmitted_30_Days']=='Yes').mean():.1%}")

# 2. FEATURE ENGINEERING
le = LabelEncoder()
df['Followup_enc'] = (df['Followup_Scheduled'] == 'Yes').astype(int)
df['Insurance_enc'] = le.fit_transform(df['Insurance_Type'])
df['Diagnosis_enc'] = le.fit_transform(df['Primary_Diagnosis'])
df['Disposition_enc'] = le.fit_transform(df['Discharge_Disposition'])
df['Gender_enc'] = le.fit_transform(df['Gender'])
df['Readmitted'] = (df['Readmitted_30_Days'] == 'Yes').astype(int)

features = ['Age', 'Length_of_Stay_Days', 'Risk_Score_at_Discharge',
            'Gender_enc', 'Followup_enc', 'Insurance_enc',
            'Diagnosis_enc', 'Disposition_enc']

X = df[features]
y = df['Readmitted']

print(f"Class balance: {y.value_counts().to_dict()}")

# 3. TRAIN/TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# 4. TRAIN RANDOM FOREST
model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)

# 5. EVALUATE
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n── Classification Report ──")
print(classification_report(y_test, y_pred,
      target_names=['Not Readmitted', 'Readmitted']))

auc = roc_auc_score(y_test, y_prob)
print(f"ROC-AUC Score: {auc:.3f}")

# 6. VISUALIZATIONS
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Hospital Readmission Prediction Model | Random Forest',
             fontsize=14, fontweight='bold')

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=['Not Readmitted', 'Readmitted'])
disp.plot(ax=axes[0], colorbar=False, cmap='Blues')
axes[0].set_title('Confusion Matrix')

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
axes[1].plot(fpr, tpr, color='#1a3a5c', lw=2, label=f'AUC = {auc:.3f}')
axes[1].plot([0, 1], [0, 1], 'k--', lw=1, label='Random baseline')
axes[1].set_xlabel('False Positive Rate')
axes[1].set_ylabel('True Positive Rate')
axes[1].set_title('ROC Curve')
axes[1].legend()

# Feature Importance
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=True)

colors = ['#1a3a5c'] * len(importance_df)
colors[-1] = '#c8401e'
colors[-2] = '#c8401e'

axes[2].barh(importance_df['Feature'], importance_df['Importance'], color=colors)
axes[2].set_title('Feature Importance\n(higher = more predictive)')
axes[2].set_xlabel('Importance Score')

plt.tight_layout()
plt.savefig('readmission_model_results.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nPlot saved: readmission_model_results.png")