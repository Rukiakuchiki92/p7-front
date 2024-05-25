import pandas as pd
import numpy as np
import streamlit as st
import requests
from joblib import load
from typing import Any, Hashable
import traceback
from fastapi import FastAPI,Form, File, UploadFile
import json
import shap
import matplotlib as plt
import seaborn as sns



# URI de base pour l'API
URI = "http://127.0.0.1:8000/"

def call_prediction_api(client_id):
    try:
        response = requests.get(f"{URI}predic_client/{client_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erreur lors de l'appel de l'API de prédiction : {e}")
        return None

def call_client_info_api(client_id):
    try:
        response = requests.get(f"{URI}client_info/{client_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erreur lors de l'appel de l'API d'informations client : {e}")
        return None

def call_shap_api(client_id):
    try:
        response = requests.get(f"{URI}Shap/{client_id}")
        response.raise_for_status()
        shap_data = response.json()
        # Vérifier si les données SHAP ont été correctement récupérées
        if "shap_values" in shap_data:
            return shap_data["shap_values"]
        else:
            st.error("Données SHAP manquantes dans la réponse de l'API.")
            return None
    except requests.RequestException as e:
        st.error(f"Erreur lors de l'appel de l'API SHAP : {e}")
        return None
    



    

def main():
    st.sidebar.title('Sommaire')
    pages = ['Modélisation']
    page = st.sidebar.radio('Aller vers la page :', pages)
    
    if page == 'Modélisation':
        st.title("Prédiction de la solvabilité du client")
        id_client = st.number_input("Entrez l'identifiant du client :", min_value=0, step=1)
        
        if st.button("Prédire"):
            prediction_data = call_prediction_api(id_client)
            if prediction_data:
                st.subheader("Résultat de la prédiction :")
                if isinstance(prediction_data, list) and len(prediction_data) > 0:
                    pred_data = prediction_data[0]
                    st.write("Identifiant client :", id_client)
                    st.write("Statut :", pred_data.get("number", "N/A"))
                    st.write("Score de prédiction :", pred_data.get("prediction", "N/A"))
                    st.write("Solvabilité :", pred_data.get("solvabilite", "N/A"))
                    st.write("Décision :", pred_data.get("decision", "N/A"))
                else:
                    st.write("Aucune donnée de prédiction disponible.")
                
                client_info_data = call_client_info_api(id_client)
                if client_info_data:
                    st.subheader("Informations du client :")
                    st.write("Âge du client :", client_info_data.get("AGE", "N/A"))
                    
                    genre_mapping = {0: "Femme", 1: "Homme"}
                    genre_label = genre_mapping.get(client_info_data.get("GENRE_M"), "N/A")
                    st.write("Genre du client :", genre_label)
                    
                    statut_marital_mapping = {
                        "STATUT_FAMILIAL_Married": "Marié(e)",
                        "STATUT_FAMILIAL_Separated": "Divorcé(e)",
                        "STATUT_FAMILIAL_Single / not married": "Célibataire",
                        "STATUT_FAMILIAL_Widow": "Veuf(ve)"
                    }
                    for colonne, label in statut_marital_mapping.items():
                        st.write(f"{label} :", "Oui" if client_info_data.get(colonne) == 1 else "Non")
                    
                    ecole_mapping = {
                        'NIVEAU_EDUCATION_Higher education': "Bac+5 ou doctorat",
                        'NIVEAU_EDUCATION_Incomplete higher': "Après Lycée sans obtention de diplôme",
                        'NIVEAU_EDUCATION_Lower secondary': 'Niveau collège',
                        'NIVEAU_EDUCATION_Secondary / secondary special': 'Niveau Lycée'
                    }
                    for colonne, label in ecole_mapping.items():
                        st.write(f"{label} :", "Oui" if client_info_data.get(colonne) == 1 else "Non")
                    
                    type_revenu_mapping = {
                        "TYPE_REVENUS_Maternity leave": "Congé de maternité",
                        "TYPE_REVENUS_Pensioner": "Retraité",
                        "TYPE_REVENUS_State servant": "Fonctionnaire",
                        "TYPE_REVENUS_Unemployed": "Sans emploi",
                        "TYPE_REVENUS_Working": "En emploi"
                    }
                    for colonne, label in type_revenu_mapping.items():
                        st.write(f"{label} :", "Oui" if client_info_data.get(colonne) == 1 else "Non")
                    
                    st.write("Nombre de personnes dans le foyer :", client_info_data.get("CNT_FAM_MEMBERS", "N/A"))
                    st.write("Années travaillées :", client_info_data.get("YEARS_EMPLOYED", "N/A"))
                    st.write("Montant du Salaire :", client_info_data.get("REVENU_TOTAL", "N/A"))
                    st.write("Montant du crédit :", client_info_data.get("TOTAL_CREDIT", "N/A"))
                    st.write("Remboursement mensuel :", client_info_data.get("REMB_MENSUEL", "N/A"))
                    
                    car_mapping = {0: "Non", 1: "Oui"}
                    car_label = car_mapping.get(client_info_data.get("PROPRIETAIRE_VOITURE_Y"), "N/A")
                    st.write("Voiture :", car_label)
                    
                shap_data = call_shap_api(id_client)
                if shap_data:
                    st.subheader("Valeurs SHAP :")
                    shap_values_df = pd.DataFrame(shap_data.items(), columns=["Feature", "SHAP Value"])
                    # Convertir les valeurs SHAP en nombres
                    shap_values_df["SHAP Value"] = shap_values_df["SHAP Value"].apply(lambda x: float(x))
                    st.dataframe(shap_values_df)

if __name__ == "__main__":
    main()