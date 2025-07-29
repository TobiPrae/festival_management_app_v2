import streamlit as st
from utils.functions import add_to_datastore
from utils.functions import require_login

require_login() 

st.set_page_config(page_title="Teilnehmer hinzufügen")
st.title("Teilnehmer hinzufügen")

st.markdown("Gib eine Liste von Namen ein (ein Name pro Zeile)")

input_text = st.text_area("Teilnehmerliste", height=200)
attending_day = st.selectbox("Teilnahmetag", ["Samstag", "Sonntag", "Beide"])
category = st.selectbox("Kategorie", ["Orga", "Gast"])

if st.button("Teilnehmer hinzufügen"):
    lines = input_text.strip().splitlines()
    new_participants = []

    for line in lines:
        name = line.strip()

        participant = {
            "name": name,
            "attending_days": attending_day,
            "count_alcoholic_bewerages": 0.0,
            "count_non_alcoholic_bewerages": 0.0,
            "category": category,
            "ticket_amount_paid": 0.0,
            "beverage_amount_paid": 0.0,
            "expenses": 0.0
        }

        # Write each new participant to Datastore
        add_to_datastore("participants", participant, "service_account_key.json")
    st.success(f"{lines} wurden hinzugefügt!")
