import streamlit as st
import pandas as pd
from utils.functions_gcp import read_from_datastore
from utils.functions_gcp import update_to_datastore
from utils.functions_gcp import delete_from_datastore
from utils.functions import require_login

require_login() 

st.set_page_config(page_title="Teilnehmer bearbeiten")
st.title("Teilnehmer bearbeiten")

participants = read_from_datastore("participants")
df = pd.DataFrame(participants)

# Prepare dropdown options
names = df["name"].tolist()
selected_name = st.selectbox("Zu bearbeitender Teilnehmer", names)

# Load either existing task or blank
participant_row = df[df["name"] == selected_name].iloc[0].to_dict()
print(participant_row)

# Editable form
with st.form("edit_or_create_task_name"):
    name = st.text_input("Name", participant_row.get("name", ""))

    attending_days_options = ["Beide", "Samstag", "Sonntag"]
    current_attending_day = participant_row.get("attending_days", "Beide")
    attending_days = st.selectbox("Teilnahmetage", attending_days_options, 
                                  index=attending_days_options.index(current_attending_day) 
                                  if current_attending_day in attending_days_options else 0)

    category_options = ["Gast", "Orga"]
    current_category = participant_row.get("category", "Gast")
    category = st.selectbox("Kategorie", category_options, 
                            index=category_options.index(current_category) 
                            if current_category in category_options else 0)



    ticket_amount_paid = st.number_input("Pauschale (Ist)", value=float(participant_row.get("ticket_amount_paid", 0)))
    count_alcoholic_bewerages = st.number_input("Alkoholische Getränke (Anzahl)", value=float(participant_row.get("count_alcoholic_bewerages", 0)))
    count_non_alcoholic_bewerages = st.number_input("Nicht-alkoholische Getränke (Anzahl)", value=float(participant_row.get("count_non_alcoholic_bewerages", 0)))
    beverage_amount_paid = st.number_input("Getränkebezahlung (Ist)", value=float(participant_row.get("beverage_amount_paid", 0)))
    
    # Buttons
    submitted = st.form_submit_button("Speichern")
    deleted = False
    deleted = st.form_submit_button("Löschen")

if submitted:
    updated_participants = {
        "name": name,
        "attending_days": attending_days,
        "category": category,
        "ticket_amount_paid": ticket_amount_paid,
        "count_alcoholic_bewerages": count_alcoholic_bewerages,
        "count_non_alcoholic_bewerages": count_non_alcoholic_bewerages,
        "beverage_amount_paid": beverage_amount_paid,
    }

    # Update existing
    entity_id = participant_row["ID"]
    update_to_datastore("participants", entity_id, updated_participants)
    st.success(f"Angaben für {name} wurden gespeichert!")

if deleted:
    delete_from_datastore("participants", participant_row["ID"])
    st.success(f"Teilnehmer {name} gelöscht!")
