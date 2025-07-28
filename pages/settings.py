import streamlit as st
from utils.functions import get_json
from utils.functions_gcp import read_from_datastore
from utils.functions_gcp import update_to_datastore
from utils.functions import require_login

require_login() 

alias_mapping = get_json("alias_mapping")
variables = read_from_datastore("variables")

st.set_page_config(page_title="Einstellungen")
st.title("Einstellungen")

updated_settings = {}

for key, value in variables[0].items():
    if key == 'ID':
        updated_settings[key] = value
    else:
        new_value = st.number_input(
            label=alias_mapping.get(key, None),
            value=float(value),
            step=0.1,
            format="%.2f"
        )
        updated_settings[key] = new_value

# Buttons
submitted = st.button("Änderungen speichern")
if submitted:
    update_to_datastore("variables", updated_settings['ID'], updated_settings)
    st.success(f"Angaben für wurden gespeichert!")