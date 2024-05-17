import pandas as pd
import numpy as np
import streamlit as st
import requests
from joblib import load
from typing import Any, Hashable
import traceback
from fastapi import FastAPI,Form, File, UploadFile
import json
URI = "http://localhost:8000/"



def send_data_to_api(endpoint):

    url = f'{URI}{endpoint}'
    # Envoyer les données à l'API
    try:
        response = requests.get(url)

        # Vérifier le code de statut de la réponse
        if response.status_code == 200:
            st.success("Données envoyées avec succès à l'API !")
            # Retourner les données reçues de l'API
            return response.json()
        else:
            st.error(f"Erreur lors de l'envoi des données à l'API. Code de statut : {response.url}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Une erreur s'est produite lors de la communication avec l'API : {e}")
        return None


def get_ids ():
    getIdsUrl = f'{URI}get_list_ids'
    response = requests.get(getIdsUrl)
    json = response.json()
    print(json)
    return json 

def get_prediction () :
    # faire en sorte de récuperer les data du front et les envoyées à l'api
    id_client = 196888
    #
    getPredictionUrl = f'{URI}get_prediction/{id_client}'
    response = requests.get(getPredictionUrl)
    json = response.json()
    print(json)
    return json 


def get_population_summary () :
    getPredictionSummaryUrl = f'{URI}get_population_summary/'
    response = requests.get(getPredictionSummaryUrl)
    json = response.json()
    print(json)
    return json 

def test():
    endpoint = "predic_client"

    with st.form("myform"):   
        id_client = st.text_input("id_client", "")
        st.form_submit_button("Soumettre")
        uri_final = f'{endpoint}/{id_client}'
        api_response = send_data_to_api(uri_final)

        if api_response:
            st.write("Données reçues de l'API :", api_response)

def get_shap () :
    pass

def info_client ():
    pass





st.sidebar.title('Sommaire')

pages = ['Contexte du projet', 'Modélisation','test']

page = st.sidebar.radio('Aller vers la page :', pages)

if page == pages[0] :
    st.write('### Contexte du projet')
    st.write('Présentation du projet ...')
    st.write('Annonce du plan')
    st.image('banque.jpg')

elif page == pages[1] :
    st.write('### Modélisation')
    #st.dataframe(df.head())
    #st.write('Dimension du dataframe :')
    #st.write(df.shape)
    ids = get_population_summary()

    st.write(ids)
elif page == pages[2]:
    st.write('# test')

    
    #if st.checkbox('Afficher les valeurs manquantes :') :
        #st.dataframe(df.isna().sum())

