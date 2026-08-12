# Analytics Module

## Overview

This module performs exploratory data analysis and predictive modeling
on the Titanic dataset.

## Files

- `01_eda.ipynb` - Exploratory data analysis, data cleaning,
  visualizations and findings.
- `02_modeling.ipynb` - Classification models, evaluation,
  class imbalance handling, hyperparameter tuning and regression.
- `titanic.csv` - Dataset used for analysis and modeling.
- `best_pipeline.joblib` - Saved final Logistic Regression pipeline.
- `README.md` - Module documentation and run instructions.

## How to Run

1. Open the project in VS Code.
2. Open `analytics/01_eda.ipynb`.
3. Run the notebook cells for exploratory analysis.
4. Open `analytics/02_modeling.ipynb`.
5. Run the notebook cells for predictive modeling.

## Classification Models

The following models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest

Class imbalance was also evaluated using:

- Baseline Logistic Regression
- Class-weight balanced Logistic Regression
- SMOTE

Random Forest hyperparameters were tuned using GridSearchCV
with 5-fold cross-validation.

## Final Recommendation

Logistic Regression was selected as the recommended classifier
because it achieved the highest F1 score among the evaluated models.

Results:

- Accuracy: 0.8090
- Precision: 0.7833
- Recall: 0.6912
- F1 Score: 0.7344
- ROC-AUC: 0.8610

The final Logistic Regression pipeline was saved as
`best_pipeline.joblib` and successfully reloaded for prediction.

## Regression

A multivariate Linear Regression model was used to predict fare.

The regression model was evaluated using:

- MAE
- RMSE
- R²
- Adjusted R²

A residual plot was also used to inspect the regression errors.