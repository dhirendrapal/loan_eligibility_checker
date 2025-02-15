import sys
import os
import json
import pytest
import joblib
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))  # Add parent directory to sys.path
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to Flask API"


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b"Ping to Flask API"


def test_prediction_success(mocker, client):
    # Create separate mock objects for different models
    mock_model = mocker.Mock()
    mock_model.predict.return_value = [1]  # Mock model prediction

    mock_encoder = mocker.Mock()
    mock_encoder.transform.return_value = [[1, 0, 1, 0, 1, 0]]  # Simulate encoding output
    mock_encoder.get_feature_names_out.return_value = ["Gender_Male", "Married_Yes", "Dependents_1",
                                                       "Education_Graduate", "Self_Employed_No", "Property_Area_Urban"]

    mock_imputer_cat = mocker.Mock()
    mock_imputer_cat.transform.return_value = [["Male", "Yes", "1", "Graduate", "No", "Urban"]]

    mock_imputer_num = mocker.Mock()
    mock_imputer_num.transform.return_value = [[5000, 0, 200, 360, 1]]  # Numerical input values

    mock_feature_names = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History",
                          "Gender_Male", "Married_Yes", "Dependents_1", "Education_Graduate", "Self_Employed_No",
                          "Property_Area_Urban"]

    # Ensure different `joblib.load()` calls return correct objects
    mocker.patch("joblib.load",
                 side_effect=[mock_model, mock_encoder, mock_imputer_cat, mock_imputer_num, mock_feature_names])

    input_data = {
        "Gender": "Male",
        "Married": "Yes",
        "Dependents": "1",
        "Education": "Graduate",
        "Self_Employed": "No",
        "Property_Area": "Urban",
        "ApplicantIncome": 5000,
        "CoapplicantIncome": 0,
        "LoanAmount": 200,
        "Loan_Amount_Term": 360,
        "Credit_History": 1
    }

    response = client.post("/predict", json=input_data)
    assert response.status_code == 200
    assert response.json == {"prediction": "Approved"}


def test_prediction_failure(client):
    input_data = {
        "Gender": "Male",
        "Married": "No",
        "Dependents": "0",
        "Education": "Not Graduate",
        "Self_Employed": "Yes",
        "ApplicantIncome": 1500,
        "CoapplicantIncome": 0,
        "LoanAmount": 200,
        "Loan_Amount_Term": 360,
        "Credit_History": 0,
        "Property_Area": "Rural"
    }
    response = client.post("/predict", json=input_data)  # Sending empty data
    assert response.status_code == 200
    assert response.json == {"prediction": "Rejected"}

def test_prediction_missing_data(client):
    response = client.post("/predict", json={})  # Sending empty data
    assert response.status_code == 400  # Expecting an internal server error due to missing data

if __name__ == "__main__":
    pytest.main()
