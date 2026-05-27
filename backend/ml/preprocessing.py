import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COLUMN = "Churn"
NUMERIC_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL_FEATURES = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService", "MultipleLines",
    "InternetService", "OnlineSecurity", "TechSupport", "Contract", "PaperlessBilling", "PaymentMethod",
]

def normalize_columns(df):
    mapping = {
        "senior_citizen": "SeniorCitizen", "monthly_charges": "MonthlyCharges",
        "total_charges": "TotalCharges", "phone_service": "PhoneService",
        "multiple_lines": "MultipleLines", "internet_service": "InternetService",
        "online_security": "OnlineSecurity", "tech_support": "TechSupport",
        "paperless_billing": "PaperlessBilling", "payment_method": "PaymentMethod",
        "contract": "Contract", "partner": "Partner", "dependents": "Dependents",
    }
    return df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})

def build_preprocessor():
    numeric_pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical_pipeline = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))])
    return ColumnTransformer([("num", numeric_pipeline, NUMERIC_FEATURES), ("cat", categorical_pipeline, CATEGORICAL_FEATURES)])

def clean_dataframe(df):
    df = normalize_columns(df.copy())
    df["TotalCharges"] = df["TotalCharges"].replace(" ", np.nan).astype(float)
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(str).replace({"0": "No", "1": "Yes", "False": "No", "True": "Yes"})
    if TARGET_COLUMN in df.columns:
        df[TARGET_COLUMN] = df[TARGET_COLUMN].map({"Yes": 1, "No": 0, 1: 1, 0: 0})
    return df

