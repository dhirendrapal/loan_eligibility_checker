from flask import Flask, request
import joblib
import pandas as pd

app=Flask(__name__)

@app.route('/')
def home():
    return("Welcome to Flask API")

@app.route('/ping')
def printflaskapi():
    return("Ping to Flask API")

@app.route("/predict",methods=["POST"])
def prediction():
    """Predict loan approval status for input data."""
    model = joblib.load("models/loan_prediction_model.pkl")
    encoder = joblib.load("models/encoder.pkl")
    imputer_cat = joblib.load("models/imputer_cat.pkl")
    imputer_num = joblib.load("models/imputer_num.pkl")
    feature_names = joblib.load("models/feature_names.pkl")

    categorical_cols = ['Gender',
                         'Married',
                         'Dependents',
                         'Education',
                         'Self_Employed',
                         'Property_Area']
    numerical_cols = ['ApplicantIncome',
                     'CoapplicantIncome',
                     'LoanAmount',
                     'Loan_Amount_Term',
                     'Credit_History']

    data = request.get_json()
    # Convert input data to DataFrame
    data_df = pd.DataFrame([data])

    # Ensure all categorical columns exist
    for col in categorical_cols:
        if col not in data_df:
            data_df[col] = np.nan
    data_df[categorical_cols] = imputer_cat.transform(data_df[categorical_cols])

    # Ensure all numerical columns exist
    for col in numerical_cols:
        if col not in data_df:
            data_df[col] = np.nan
    data_df[numerical_cols] = imputer_num.transform(data_df[numerical_cols])

    # Encode categorical variables
    categorical_encoded = encoder.transform(data_df[categorical_cols])
    categorical_df = pd.DataFrame(categorical_encoded, columns=encoder.get_feature_names_out(categorical_cols))

    # Merge numerical and categorical features
    X_input = pd.concat([data_df[numerical_cols].reset_index(drop=True), categorical_df], axis=1)

    # Ensure correct column order
    for col in feature_names:
        if col not in X_input:
            X_input[col] = 0  # Add missing features with default value
    X_input = X_input[feature_names]

    # Predict
    prediction = model.predict(X_input)

    if prediction==0:
        pred="Rejected"
    else:
        pred="Approved"

    return{"prediction":pred}