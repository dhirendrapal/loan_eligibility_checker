# Loan eligibility checker
This repository contains the code for a loan eligibility checker, designed to assess applicants' eligibility based on predefined criteria.

## Initial setup
```
python3.10 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

# Loan Prediction Model

## To Create Model
1. Install Jupyter Notebook:
   ```bash
   pip install jupyter notebook
   ```
2. Start Jupyter Notebook:
   ```bash
   python -m notebook
   ```
3. Run the notebook:
   ```
   notebooks/Loan_pred.ipynb
   ```
4. After running `Loan_pred.ipynb`, all related files will be saved in the `models` directory.

## To Access API
1. Start Flask server:
   ```bash
   flask run
   ```
2. To run a prediction, use the following URL:
   ```
   http://127.0.0.1:5000/predict
   ```
3. Example Request Body:
   ```json
   {
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
