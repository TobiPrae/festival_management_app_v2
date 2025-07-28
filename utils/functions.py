
import json
import streamlit as st

def get_json(file_name):
    """
    Loads data from json
    """

    # Load JSON file
    with open(f'data/{file_name}.json', 'r') as f:
        json_output = json.load(f)

    return json_output

def require_login():
    users = st.secrets.get("users", {})

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Login erforderlich")
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        if st.button("Anmelden"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Ungültiger Benutzername oder Passwort")
        st.stop()

    # Sidebar logout button
    st.sidebar.success(f"Angemeldet als: {st.session_state.username}")
    if st.sidebar.button("Abmelden"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()