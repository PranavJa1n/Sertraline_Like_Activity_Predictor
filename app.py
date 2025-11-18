from flask import Flask, render_template, request
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import uvicorn
from asgiref.wsgi import WsgiToAsgi

app = Flask(__name__)

with open('models/XGBoost_Model.pkl', 'rb') as m:
    XGB_model = pickle.load(m)
with open("models/Random_Forest_Model.pkl","rb") as m:
    RF_model = pickle.load(m)
with open("models/support_vector_machine_Model.pkl","rb") as m:
    SVM_model = pickle.load(m)
with open("models/logistic_regression_model.pkl", "rb") as m:
    LR_model = pickle.load(m)
with open('models/feature.pkl', 'rb') as f:
    feature_names = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/predict', methods=['POST'])
def predict():
    smiles = request.form['smiles']
    print(f"Received SMILES: {smiles}")
    selected_value = request.form['my_dropdown']
    print(f"Selected Model: {selected_value}")
    fingerprint = []
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return render_template('index.html', error="Invalid SMILES string! Please check and try again.", smiles=smiles, selected_model=selected_value)
    morgan_fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
    fingerprint.append(list(morgan_fp))
    fingerprint_df = pd.DataFrame(fingerprint, columns=[f'FP_{i}' for i in range(2048)])
    
    num_h_donors = []
    num_h_acceptors = []
    tpsa = []
    num_rotatable_bonds = []
    num_aromatic_rings = []
    num_saturated_rings = []
    num_aliphatic_rings = []
    num_heteroatoms = []
    mol_logp = []
    num_rings = []
    mol_weight = []
    num_h_donors.append(Descriptors.NumHDonors(mol))
    num_h_acceptors.append(Descriptors.NumHAcceptors(mol))
    tpsa.append(Descriptors.TPSA(mol))
    num_rotatable_bonds.append(Descriptors.NumRotatableBonds(mol))
    num_aromatic_rings.append(Descriptors.NumAromaticRings(mol))
    num_saturated_rings.append(Descriptors.NumSaturatedRings(mol))
    num_aliphatic_rings.append(Descriptors.NumAliphaticRings(mol))
    num_heteroatoms.append(Descriptors.NumHeteroatoms(mol))
    mol_logp.append(Descriptors.MolLogP(mol))
    num_rings.append(Descriptors.RingCount(mol))
    mol_weight.append(Descriptors.MolWt(mol))
    desc_df = pd.DataFrame({
        'NumHDonors': num_h_donors,
        'NumHAcceptors': num_h_acceptors,
        'TPSA': tpsa,
        'NumRotatableBonds': num_rotatable_bonds,
        'NumAromaticRings': num_aromatic_rings,
        'NumSaturatedRings': num_saturated_rings,
        'NumAliphaticRings': num_aliphatic_rings,
        'NumHeteroatoms': num_heteroatoms,
        'MolLogP': mol_logp,
        'NumRings': num_rings,
        "Molecular Weight" : mol_weight
    })
    print(f"Description values: {desc_df}")
    features = pd.concat([desc_df, fingerprint_df], axis=1)
    feature_vector = pd.DataFrame(features, columns=feature_names)
    
    if selected_value == "svm":
        prediction = SVM_model.predict(feature_vector)[0]
        print(f"Prediction: {prediction}")
        result = {
            'smiles': smiles,
            'prediction': 'ACTIVE' if prediction == 1 else 'INACTIVE',
            'prediction_class': prediction,
            'probability_active': 0.0,
            'probability_inactive': 0.0,
            'confidence': 0.0,
            'mol_weight': round(mol_weight[0], 2),
            'logp': round(mol_logp[0], 2),
            'h_donors': desc_df['NumHDonors'].iloc[0],
            'h_acceptors': desc_df['NumHAcceptors'].iloc[0],
            'tpsa': round(desc_df['TPSA'].iloc[0], 2),
            'rotatable_bonds': desc_df['NumRotatableBonds'].iloc[0],
            'aromatic_rings': desc_df['NumAromaticRings'].iloc[0],
            'total_rings': desc_df['NumRings'].iloc[0],
            'model': selected_value.upper()
        }
        return render_template('index.html', result=result)
    elif selected_value == "xg" :
        prediction = XGB_model.predict(feature_vector)[0]
        probability = XGB_model.predict_proba(feature_vector)[0]
    elif selected_value == "rf":
        prediction  = RF_model.predict(feature_vector)[0]
        probability = RF_model.predict_proba(feature_vector)[0]
    elif selected_value == "lr":
        prediction = LR_model.predict(feature_vector)[0]
        probability = LR_model.predict_proba(feature_vector)[0]   

    print(f"Prediction: {prediction}")
    print(f"Probability: {probability}")
    
    result = {
        'smiles': smiles,
        'prediction': 'ACTIVE' if prediction == 1 else 'INACTIVE',
        'prediction_class': prediction,
        'probability_active': round(probability[1] * 100, 2),
        'probability_inactive': round(probability[0] * 100, 2),
        'confidence': round(max(probability) * 100, 2),
        'mol_weight': round(mol_weight[0], 2),
        'logp': round(mol_logp[0], 2),
        'h_donors': desc_df['NumHDonors'].iloc[0],
        'h_acceptors': desc_df['NumHAcceptors'].iloc[0],
        'tpsa': round(desc_df['TPSA'].iloc[0], 2),
        'rotatable_bonds': desc_df['NumRotatableBonds'].iloc[0],
        'aromatic_rings': desc_df['NumAromaticRings'].iloc[0],
        'total_rings': desc_df['NumRings'].iloc[0],
        'model': selected_value.upper()
    }
    
    return render_template('index.html', result=result)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True)
    app = WsgiToAsgi(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)