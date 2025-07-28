import streamlit as st
import pandas as pd
from utils.functions import get_json
from utils.functions_gcp import read_from_datastore
from utils.functions_gcp import update_to_datastore
from utils.functions_gcp import delete_from_datastore
from utils.functions_gcp import add_to_datastore
from utils.functions import require_login

require_login() 

# Read data from datastore and set variables
todos = read_from_datastore("todos")
participants = read_from_datastore("participants")
participant_names = [p["name"] for p in participants if p.get("category") == "Orga"] + ["tbd"]
alias_mapping = get_json("alias_mapping")

st.set_page_config(page_title="Planung")
st.title("Planung")

# Load and convert to DataFrame
df = pd.DataFrame(todos)
display_cols = ["task", "category", "responsible", "done", "paid", "description", "quantity", "estimated_price", "estimated_cost", "actual_cost"]

# Filtering part
st.sidebar.header("Filteroptionen")

responsible_options = ["Alle"] + sorted(df["responsible"].dropna().unique().tolist())
selected_responsible = st.sidebar.selectbox("Verantwortlich", responsible_options)

done_options = ["Alle"] + sorted(df["done"].dropna().unique().tolist())
selected_done = st.sidebar.selectbox("Erledigt", done_options)

category_options = ["Alle"] + sorted(df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Kategorie", category_options)

paid_options = ["Alle"] + sorted(df["paid"].dropna().unique().tolist())
selected_paid = st.sidebar.selectbox("Ausbezahlt", paid_options)

# Apply filters
filtered_df = df.copy()
if selected_responsible != "Alle":
    filtered_df = filtered_df[filtered_df["responsible"] == selected_responsible]
if selected_done != "Alle":
    filtered_df = filtered_df[filtered_df["done"] == selected_done]
if selected_category != "Alle":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
if selected_paid != "Alle":
    filtered_df = filtered_df[filtered_df["paid"] == selected_paid]

# Show filtered data
st.dataframe(filtered_df[display_cols].rename(columns=alias_mapping), use_container_width=True)

with st.expander("**Hinzufügen oder bearbeiten**", expanded=False):
    # Prepare dropdown options
    task_names = filtered_df["task"].tolist()
    task_options = ["Neu"] + task_names
    selected_task = st.selectbox("Zu bearbeitender Task", task_options)

    # Define blank template for a new task
    blank_task = {
        "task": "Default Aufgabe",
        "responsible": "tbd",
        "done": False,
        "paid": False,
        "category": "Sonstige",
        "description": "",
        "quantity": 0.0,
        "estimated_price": 0.0,
        "estimated_cost": 0.0,
        "actual_cost": 0.0,
        "ID": 0
    }

    # Load either existing task or blank
    if selected_task == "Neu":
        task_row = blank_task
    else:
        task_row = filtered_df[filtered_df["task"] == selected_task].iloc[0].to_dict()
    # Editable form
    with st.form("edit_or_create_task_form"):
        task = st.text_input("Task", task_row.get("task", ""))
        responsible = st.selectbox("Verantwortlich", participant_names, index=participant_names.index(task_row.get("responsible", "tbd")) if task_row.get("responsible") in participant_names else len(participant_names) - 1)
        done = st.selectbox("Erledigt", [True, False], index=0 if task_row.get("done") else 1)
        paid = st.selectbox("Ausbezahlt", [True, False], index=0 if task_row.get("paid") else 1)
        category_options = ["Sonstiges", "Essen", "Getränke"]
        current_category = task_row.get("category", "Sonstiges")
        category = st.selectbox("Kategorie", category_options, 
                            index=category_options.index(current_category) 
                            if current_category in category_options else 0)
        description = st.text_area("Beschreibung", task_row.get("description", ""))
        quantity = st.number_input("Menge", value=float(task_row.get("quantity", 0)))
        estimated_price = st.number_input("Geschätzter Preis", value=float(task_row.get("estimated_price", 0)))
        actual_cost = st.number_input("Tatsächliche Kosten", value=float(task_row.get("actual_cost", 0)))
        
        # Buttons
        submitted = st.form_submit_button("Speichern")
        deleted = False
        if selected_task != "Neu":
            deleted = st.form_submit_button("Löschen")

if submitted:
    updated_task = {
        "task": task,
        "responsible": responsible,
        "done": done,
        "paid": paid,
        "category": category,
        "description": description,
        "quantity": quantity,
        "estimated_price": estimated_price,
        "estimated_cost": estimated_price*quantity,
        "actual_cost": actual_cost,
    }

    # Update existing
    if selected_task != "Neu":
        entity_id = task_row["ID"]
        update_to_datastore("todos", entity_id, updated_task)
        st.rerun()
    else:
        add_to_datastore("todos", updated_task)
        st.rerun()

if deleted:
    if selected_task != "Neu":
        delete_from_datastore("todos", task_row["ID"])
        st.rerun()
    else:
        st.warning("Kein Eintrag zum Löschen ausgewählt.")
