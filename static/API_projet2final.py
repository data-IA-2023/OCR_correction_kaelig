# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:00:58 2024

@author: kaeli
"""

import streamlit as st
import pandas as pd
import pickle

















with open('modele_projet2.pkl', 'rb') as model:
    model = pickle.load(model)


st.title("Rentrer le message que vous voulez tester")

if 'model' not in st.session_state:
    st.session_state.model=model
    
if 'df_message' not in st.session_state:
    st.session_state.df_message = pd.DataFrame(columns=['contenus'])

st.session_state.user_input = st.text_input("Entrez le message que vous voulez tester ici:")

if st.button("Enregistrer"):
    st.session_state.df_inter_message=pd.DataFrame(data=[st.session_state.user_input],columns=['contenus'])
    st.session_state.df_message = pd.concat([st.session_state.df_message, st.session_state.df_inter_message])
    st.session_state.X=st.session_state.df_message['contenus']
    if st.session_state.X.empty:
        st.warning("Aucune donnée à prédire. Veuillez entrer des données.")
    else:
        st.session_state.predictions = st.session_state.model.predict(st.session_state.X.to_frame())
        st.session_state.df_message['Prediction'] = st.session_state.predictions
    
st.dataframe(st.session_state.df_message)