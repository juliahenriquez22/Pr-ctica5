
import mysql.connector
import streamlit as st

st.title("Conexión con base de datos MySQL")

# Obtener credenciales de Streamlit Secrets
host = st.secrets["mysql"]["host"]
port = st.secrets["mysql"]["port"]
user = st.secrets["mysql"]["user"]
password = st.secrets["mysql"]["password"]
database = st.secrets["mysql"]["database"]

try:
    conn = mysql.connector.connect(
        host=host,
        port=int(port),
        user=user,
        password=password,
        database=database,
        connection_timeout=10
    )

    if conn.is_connected():
        st.success("¡Conexión exitosa con MySQL!")

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()

        st.subheader("Tablas de la base de datos")

        if tablas:
            for tabla in tablas:
                st.write(tabla[0])
        else:
            st.info("La base de datos todavía no tiene tablas.")

        cursor.close()
        conn.close()

except mysql.connector.Error as error:
    st.error(f"Error de conexión: {error}")
except Exception as error:
    st.error(f"Revisá la configuración: {error}")
