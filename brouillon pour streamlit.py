
def main():
    st.title("Prédiction de la solvabilité du client")
    
    id_client = st.number_input("Entrez l'identifiant du client :", min_value=0, step=1)
    
    if st.button("Prédire"):
        data = call_api(id_client)
        if data:
            st.subheader("Résultat de la prédiction :")
            st.write("Identifiant client :", id_client)
            st.write("Statut :", data[0]["number"])
            st.write("Score de prédiction :", data[0]["prediction"])
            st.write("Solvabilité :", data[0]["solvabilite"])
            st.write("Décision :", data[0]["decision"])
        else:
            st.write("Erreur lors de la récupération des données. Veuillez réessayer plus tard.")



CELLE QUI FONCTIONNE 100%




# Définir la fonction pour appeler l'API
def call_api(endpoint, id_client):
    url = URI + endpoint + str(id_client)
    response = requests.get(url)
    data = response.json()
    return data

def main():
    st.sidebar.title('Sommaire')

    # Définir le nom de la page
    pages = ['Modélisation']

    # Sélection de la page dans la barre latérale
    page = st.sidebar.radio('Aller vers la page :', pages)

    # Afficher le contenu en fonction de la page sélectionnée
    if page == 'Modélisation':
        st.title("Prédiction de la solvabilité du client")

        # Saisie de l'identifiant du client
        id_client = st.number_input("Entrez l'identifiant du client :", min_value=0, step=1)
        
        # Bouton pour déclencher la prédiction
        if st.button("Prédire"):
            # Appel de l'API pour récupérer les données de prédiction
            data = call_api("predic_client/", id_client)
            if data:
                # Affichage des résultats de la prédiction
                st.subheader("Résultat de la prédiction :")
                st.write("Identifiant client :", id_client)
                st.write("Statut :", data[0]["number"])
                st.write("Score de prédiction :", data[0]["prediction"])
                st.write("Solvabilité :", data[0]["solvabilite"])
                st.write("Décision :", data[0]["decision"])
            else:
                st.write("Erreur lors de la récupération des données. Veuillez réessayer plus tard.")

# Exécution de l'application Streamlit
if __name__ == "__main__":
    main()