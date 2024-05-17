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




# URI de base pour l'API
URI = "http://localhost:8000/"

# Fonction pour appeler l'API et récupérer les données de prédiction
def call_prediction_api(client_id):
    endpoint = f"predic_client/{client_id}"
    url = URI + endpoint
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erreur lors de l'appel de l'API de prédiction :", response.text)
        return None

# Fonction pour appeler l'API et récupérer les informations du client
def call_client_info_api(client_id):
    endpoint = f"client_info/{client_id}"
    url = URI + endpoint
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erreur lors de l'appel de l'API d'informations client :", response.text)
        return None

    



# Fonction principale de l'application Streamlit
def main():
    st.sidebar.title('Sommaire')

    # Nom de la page
    pages = ['Modélisation']

    # Sélection de la page dans la barre latérale
    page = st.sidebar.radio('Aller vers la page :', pages)

    # Affichage du contenu en fonction de la page sélectionnée
    if page == 'Modélisation':
        st.title("Prédiction de la solvabilité du client")

        # Saisie de l'identifiant du client
        id_client = st.number_input("Entrez l'identifiant du client :", min_value=0, step=1)
        
        # Bouton pour déclencher la prédiction
        if st.button("Prédire"):
            # Appel de l'API pour récupérer les données de prédiction
            prediction_data = call_prediction_api(id_client)
            if prediction_data:
                # Affichage des résultats de la prédiction
                st.subheader("Résultat de la prédiction :")
                if isinstance(prediction_data, list) and len(prediction_data) > 0:
                    pred_data = prediction_data[0]  # Extraire les données de prédiction du premier élément de la liste
                    st.write("Identifiant client :", id_client)
                    st.write("Statut :", pred_data.get("number", "N/A"))
                    st.write("Score de prédiction :", pred_data.get("prediction", "N/A"))
                    st.write("Solvabilité :", pred_data.get("solvabilite", "N/A"))
                    st.write("Décision :", pred_data.get("decision", "N/A"))
                else:
                    st.write("Aucune donnée de prédiction disponible.")
                
                # Appel de l'API pour récupérer les informations du client
                client_info_data = call_client_info_api(id_client)
                
                if client_info_data:
                # Affichage des informations du client
                    st.subheader("Informations du client :")
                    st.write("Âge du client :", client_info_data.get("AGE", "N/A"))
    
                    # Mapping du genre
                    genre_mapping = {0: "Femme", 1: "Homme"}
                    genre_code = client_info_data.get("GENRE_M", None)
                    genre_label = genre_mapping.get(genre_code, "N/A")
                    st.write("Genre du client :", genre_label)


                    # Mapping pour le statut marital
                    statut_marital_mapping = {
                        "STATUT_FAMILIAL_Married": "Marié(e)",
                        "STATUT_FAMILIAL_Separated": "Divorcé(e)",
                        "STATUT_FAMILIAL_Single / not married": "Célibataire",
                        "STATUT_FAMILIAL_Widow": "Veuf(ve)"
                                                            }

                    # Liste des colonnes de statut marital
                    colonnes_statut_marital = ["STATUT_FAMILIAL_Married", "STATUT_FAMILIAL_Separated", "STATUT_FAMILIAL_Single / not married", "STATUT_FAMILIAL_Widow"]
                    
                    # Parcourir chaque colonne de statut marital
                    for colonne in colonnes_statut_marital:
                        # Récupérer la valeur du statut marital pour cette colonne
                        valeur_statut_marital = client_info_data.get(colonne, None)
                        
                        # Appliquer le mapping pour obtenir le libellé du statut marital
                        label_statut_marital = statut_marital_mapping.get(colonne, "N/A")
    
                        # Afficher le libellé du statut marital pour cette colonne
                        st.write(f"{label_statut_marital} :", "Oui" if valeur_statut_marital == 1 else "Non")


                    # Mapping pour le niveau d'éducation
                    ecole_mapping = {
                        'NIVEAU_EDUCATION_Higher education' : "Bac+5 ou doctorat",
                        'NIVEAU_EDUCATION_Incomplete higher' : "Après Lycée sans obtention de diplôme",
                        'NIVEAU_EDUCATION_Lower secondary' : 'Niveau collège',
                        'NIVEAU_EDUCATION_Secondary / secondary special' : 'Niveau Lycée'
                                                            }

                    # Liste des colonnes de statut marital
                    colonnes_ecole = ["NIVEAU_EDUCATION_Higher education", "NIVEAU_EDUCATION_Incomplete higher", "NIVEAU_EDUCATION_Lower secondary", "NIVEAU_EDUCATION_Secondary / secondary special"]
                    
                    # Parcourir chaque colonne de statut marital
                    for colonne in colonnes_ecole:
                        # Récupérer la valeur du statut marital pour cette colonne
                        valeur_statut_ecole = client_info_data.get(colonne, None)
                        
                        # Appliquer le mapping pour obtenir le libellé du statut marital
                        label_ecole = ecole_mapping.get(colonne, "N/A")
    
                        # Afficher le libellé du statut marital pour cette colonne
                        st.write(f"{label_ecole} :", "Oui" if valeur_statut_ecole == 1 else "Non")


                    # Mapping pour le niveau d'éducation
                    type_revenu_mapping = {
                        "TYPE_REVENUS_Maternity leave" : "Congé de maternité",
                        "TYPE_REVENUS_Pensioner" : "Retraité",
                        "TYPE_REVENUS_State servant" : "Fonctionnaire",
                        "TYPE_REVENUS_Unemployed" : "Sans emploi",
                        "TYPE_REVENUS_Working" : "En emploi",
                                                            }

                    # Liste des colonnes de statut marital
                    colonnes_type_revenu = [ 'TYPE_REVENUS_Maternity leave', 'TYPE_REVENUS_Pensioner',
                                        'TYPE_REVENUS_State servant', 'TYPE_REVENUS_Unemployed',
                                        'TYPE_REVENUS_Working']
                    
                    # Parcourir chaque colonne de statut marital
                    for colonne in colonnes_type_revenu:
                        # Récupérer la valeur du statut marital pour cette colonne
                        valeur_type_revenu = client_info_data.get(colonne, None)
                        
                        # Appliquer le mapping pour obtenir le libellé du statut marital
                        label_type_revenu = type_revenu_mapping.get(colonne, "N/A")
    
                        # Afficher le libellé du statut marital pour cette colonne
                        st.write(f"{label_type_revenu} :", "Oui" if valeur_type_revenu == 1 else "Non")














                    st.write("Nombre de personnes dans le foyer :", client_info_data.get("CNT_FAM_MEMBERS", "N/A"))
                    st.write("Années travaillées :", client_info_data.get("YEARS_EMPLOYED", "N/A"))
                    st.write("Montant du Salaire :", client_info_data.get("REVENU_TOTAL", "N/A"))

                    
                    st.write("Montant du crédit :", client_info_data.get("TOTAL_CREDIT", "N/A"))
                    st.write("Remboursement mensuel :", client_info_data.get("REMB_MENSUEL", "N/A"))

                    # Mapping pour propriétaire voiture
                    car_mapping = {0: "Non", 1: "Oui"}
                    car_code = client_info_data.get("PROPRIETAIRE_VOITURE_Y", None)
                    car_label = car_mapping.get(car_code, "N/A")
                    st.write("Voiture :", car_label)


                
        else:
                st.write("Erreur lors de la récupération des données. Veuillez réessayer plus tard.")

# Exécution de l'application Streamlit
if __name__ == "__main__":
    main()