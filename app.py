import mysql.connector 

import streamlit as st 

st.title("Conexión con base de datos MySQL") 

# Obtener las credenciales almacenadas en Streamlit Secrets 

host = st.secrets["mysql"]["host"] 

port = st.secrets["mysql"]["port"] 

user = st.secrets["mysql"]["user"] 

password = st.secrets["mysql"]["password"] 

database = st.secrets["mysql"]["database"] 

# Intentar establecer la conexión 

try: 

    conn = mysql.connector.connect( 

        host=host, 

        port=port, 

        user=user, 

        password=password, 

        database=database 
