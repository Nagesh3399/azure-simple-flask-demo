import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
import joblib  # for saving model and pipeline
from fetch_data import fetch_table_as_df
# Assuming train_df and test_df are loaded as you showed

train_df = fetch_table_as_df("cleaned_train")
test_df = fetch_table_as_df("cleaned_test")


def preprocess_and_train(train_df, test_df):

    # Drop columns not useful as features
    drop_cols = ['mobile_number']
    # Assuming date columns start with 'last_date_of_month_'
    date_cols = [col for col in train_df.columns if col.startswith('last_date_of_month_')]

    # Drop these columns from both train and test
    train_df = train_df.drop(columns=drop_cols + date_cols)
    test_df = test_df.drop(columns=drop_cols + date_cols)

    # Separate features and target
    X_train = train_df.drop('churn', axis=1)
    y_train = train_df['churn']

    X_test = test_df.drop('churn', axis=1)
    y_test = test_df['churn']

    # Identify numeric columns
    numeric_features = X_train.select_dtypes(include=[np.number]).columns.tolist()

    # Simple numeric pipeline: impute missing values with median + standard scaling
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Full preprocessing pipeline
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features)
    ])

    # Decision Tree pipeline
    dt_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', DecisionTreeClassifier(random_state=42))
    ])

    # Train Decision Tree
    dt_pipeline.fit(X_train, y_train)
    y_pred_dt = dt_pipeline.predict(X_test)
    print("Decision Tree Classification Report:")
    print(classification_report(y_test, y_pred_dt))

    # Gradient Boosting pipeline
    gb_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', GradientBoostingClassifier(random_state=42))
    ])

    # Train Gradient Boosting
    gb_pipeline.fit(X_train, y_train)
    y_pred_gb = gb_pipeline.predict(X_test)
    print("Gradient Boosting Classification Report:")
    print(classification_report(y_test, y_pred_gb))

    # Save pipelines/models for later use in Flask
    joblib.dump(dt_pipeline, 'dt_pipeline.pkl')
    joblib.dump(gb_pipeline, 'gb_pipeline.pkl')
    print("Models saved: dt_pipeline.pkl, gb_pipeline.pkl")

    return dt_pipeline, gb_pipeline

# Call this function with your dataframes
dt_model, gb_model = preprocess_and_train(train_df, test_df)
