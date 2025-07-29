import streamlit as st
import numpy as np
from utils.functions import get_json
import pandas as pd
from utils.functions import read_from_datastore
from utils.functions import update_to_datastore
from utils.functions import require_login

require_login() 

# Read data from datastore and set variables
expenses = read_from_datastore("expenses")
alias_mapping = get_json("alias_mapping")
participants = read_from_datastore("participants")

st.set_page_config(page_title="Ausgaben")
st.title("Ausgaben")

# Load and convert to DataFrame
df_participants = pd.DataFrame(participants)
revenue = df_participants["beverage_amount_paid"].sum() + df_participants["ticket_amount_paid"].sum()
df_expenses = pd.DataFrame(expenses)
df_expenses["paid"] = df_expenses["actual_cost_paid"] >= df_expenses["actual_cost"]
total_paid = df_expenses["actual_cost_paid"].sum()

# Apply filters
df_expenses = df_expenses.sort_values(by=["actual_cost"], ascending=[ False])

col1, col2 = st.columns([2, 1])
with col1:
    st.write(f"Gesamteinnahmen")
    st.write(f"\\- Kosten Ausbezahlt")
    st.write(f"**= Rest**")
with col2:
    st.write(f"{revenue:.2f} €")
    st.write(f"{total_paid:.2f} €")
    st.write(f"**{revenue - total_paid:.2f} €**")

# Show filtered data
st.dataframe(df_expenses[["responsible", "actual_cost", "actual_cost_paid", "paid"]].rename(columns=alias_mapping), use_container_width=True)

with st.expander("**Bearbeiten**", expanded=False):
    # --- Step 2: Create a list of responsibles ---
    responsibles = sorted([e["responsible"] for e in expenses if "responsible" in e])

    selected_responsible = st.selectbox("Bezahlung für Person ändern:", responsibles)

    responsible_row = df_expenses[df_expenses["responsible"] == selected_responsible].iloc[0].to_dict()

    # Editable form
    with st.form("edit_or_create_task_form"):
        actual_cost = st.number_input("Tatsächliche Kosten (€)", value=float(responsible_row.get("actual_cost", 0)), disabled=True)
        actual_cost_paid = st.number_input("Kosten Ausbezahlt (€)", value=float(responsible_row.get("actual_cost_paid", 0)))

        # Buttons
        submitted = st.form_submit_button("Speichern")

    if submitted:
        updated_expenses = {
        "responsible": selected_responsible,
        "actual_cost": actual_cost,
        "actual_cost_paid": actual_cost_paid
        }

        entity_id = responsible_row["ID"]
        update_to_datastore("expenses", entity_id, updated_expenses)
        st.rerun()

