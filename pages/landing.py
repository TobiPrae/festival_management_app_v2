import streamlit as st
from utils.functions import require_login

require_login() 

st.title("Kommunenzeltfest 2026")

st.markdown("""
Willkommen zur Organisationsplattform des **Kommunenzeltfests**!

Hier findest du alle wichtigen Informationen zur Planung, Teilnehmerkoordination und dem Ablauf des Festivals.

---     
 
""")
st.markdown(
    """
    <a href="https://github.com/TobiPrae" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-TobiPrae-181717?style=for-the-badge&logo=github">
    </a>
    """,
    unsafe_allow_html=True
)
