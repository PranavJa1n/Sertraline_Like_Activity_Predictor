# Sertraline-Like Activity Predictor

A Flask-based QSAR (Quantitative Structure–Activity Relationship) web application that predicts whether a molecule (provided as a SMILES string) shows sertraline like activities . The app computes molecular descriptors and fingerprints using RDKit and runs trained ML models (XGBoost, Random Forest, SVM, Logistic Regression) to produce a prediction and related metrics.

**Key features**
- Real-time SMILES input and activity prediction via web UI
- Multiple pre-trained models: XGBoost, Random Forest, SVM, Logistic Regression
- Molecular descriptors + Morgan fingerprint (2048 bits) as features
- Interactive UI with confidence and probability output

**Repository structure (important files & folders)**
- `app.py` : Flask app + prediction endpoint (uses RDKit and pre-trained models in `models/`).
- `requirements.txt` : Python dependencies.
- `dockerfile` : Dockerfile to build a container image.
- `models/` : Pickled trained models and `feature.pkl` (ordered feature names used at inference).
- `dataCollectionAndPreprocessing/` : Raw and cleaned data + preprocessing notebooks.
- `modelDevelopment/` : Notebooks used for feature engineering and model development.
- `templates/index.html` and `static/style.css` : Web UI templates & styles.

Models included (in `models/`):
- `XGBoost_Model.pkl`
- `Random_Forest_Model.pkl`
- `support_vector_machine_Model.pkl`
- `logistic_regression_model.pkl`
- `naive_bayes.pkl`
- `feature.pkl` (feature order used by models)

Notes about the environment
- RDKit is required by `app.py`. On many platforms RDKit is easiest installed via conda. Installing RDKit with pip may not be straightforward.

Quick start — Local Python (recommended for development)

1. Create and activate a virtual environment (bash examples):

```bash
python -m venv .venv
source .venv/Scripts/activate   # Linux or Windows (Git Bash)
.venv/Scripts/activate   # Windows
```

2. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the app locally:

```bash
python app.py
# App will start on http://0.0.0.0:8000 by default (uvicorn)
```

4. Open a browser and go to `http://localhost:8000` to use the UI.

Docker (build & run)

```bash
docker build -t ml-project .
docker run -p 8000:8000 ml-project
```

How to use the UI/API
- Visit `/` to open the web UI. Provide a valid SMILES string and select a model from the dropdown, then submit.
- The form posts to `/predict` with fields:
  - `smiles` — SMILES string input
  - `my_dropdown` — model selector (`xg`, `rf`, `lr`, `svm`, ...)

Data and model development
- Raw and cleaned datasets, plus notebooks used for preprocessing and model training, are in:
  - `dataCollectionAndPreprocessing/`
  - `modelDevelopment/`

Project Structure (detailed)
```
Sertraline_Like_Activity_Predictor/
├─ app.py                       # Flask app and prediction endpoint
├─ dockerfile                   # Dockerfile to containerize the app
├─ requirements.txt             # Python dependencies
├─ README.md                    # Project README (this file)
├─ templates/
│  └─ index.html                # Frontend template for the web UI
├─ static/
│  └─ style.css                 # CSS for UI
├─ models/                      # Pickled models and feature order
│  ├─ XGBoost_Model.pkl
│  ├─ Random_Forest_Model.pkl
│  ├─ support_vector_machine_Model.pkl
│  ├─ logistic_regression_model.pkl
│  ├─ naive_bayes.pkl
│  └─ feature.pkl
├─ dataCollectionAndPreprocessing/
│  ├─ Raw_SERT_data.csv
│  ├─ Cleaned_SERT_Data.csv
│  └─ cleaning.ipynb
└─ modelDevelopment/
   ├─ Ready_Data.csv
   ├─ features.ipynb
   ├─ decisionTrees.ipynb
   ├─ randomForest.ipynb
   ├─ logisticRegression.ipynb
   ├─ naiveBayes.ipynb
   ├─ supportVectorMachine.ipynb
   └─ XGBoost.ipynb

```
