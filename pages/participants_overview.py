import streamlit as st
import pandas as pd
import numpy as np
from utils.functions import get_json
from utils.functions import read_from_datastore
from utils.functions import require_login

require_login() 

# Read data from datastore and set variables
variables = read_from_datastore("variables")[0]
participants = read_from_datastore("participants")
alias_mapping = get_json("alias_mapping")

st.set_page_config(page_title="Teilnehmerübersicht")
st.title("Teilnehmerübersicht")

# Convert to DataFrame
df = pd.DataFrame(participants)

# Create new columns
df["beverage_amount_target"] = (df["count_alcoholic_bewerages"] * variables['alcoholic_beverage_price']) + (df["count_non_alcoholic_bewerages"] * variables['non_alcoholic_beverage_price']) + (df["count_weisswurst"] * variables['weisswurst_price'])

df["ticket_amount_target"] = np.where(df["attending_days"] == "Beide", variables['two_day_ticket'], variables['one_day_ticket']) 

df["beverages_fully_paid"] = df["beverage_amount_target"] <= df['beverage_amount_paid']
df["ticket_fully_paid"] = df["ticket_amount_target"] <= df['ticket_amount_paid']

# Reorder columns for display
display_cols = ["name",
                "category", 
                "attending_days",
                "ticket_fully_paid",
                "beverages_fully_paid",
                "ticket_amount_target",
                "ticket_amount_paid",
                "count_alcoholic_bewerages",
                "count_non_alcoholic_bewerages",
                "count_weisswurst",
                "beverage_amount_target",
                "beverage_amount_paid",
]

# Sidebar filters
st.sidebar.header("Filteroptionen")

attending_options = ["Alle"] + sorted(df["attending_days"].dropna().unique().tolist())
selected_day = st.sidebar.selectbox("Teilnahmetage", attending_options)

category_options = ["Alle"] + sorted(df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Kategorie", category_options)

ticket_fully_paid_options = ["Alle"] + sorted(df["ticket_fully_paid"].dropna().unique().tolist())
selected_ticket_fully_paid_options = st.sidebar.selectbox("Pauschale vollständig bezahlt", ticket_fully_paid_options)

beverages_fully_paid_options = ["Alle"] + sorted(df["beverages_fully_paid"].dropna().unique().tolist())
selected_beverages_fully_paid_options = st.sidebar.selectbox("Getränke vollständig bezahlt", beverages_fully_paid_options)

# Apply filters
filtered_df = df.copy()
if selected_day != "Alle":
    filtered_df = filtered_df[filtered_df["attending_days"] == selected_day]
if selected_category != "Alle":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]
if selected_ticket_fully_paid_options != "Alle":
    filtered_df = filtered_df[filtered_df["ticket_fully_paid"] == selected_ticket_fully_paid_options]
if selected_beverages_fully_paid_options != "Alle":
    filtered_df = filtered_df[filtered_df["beverages_fully_paid"] == selected_beverages_fully_paid_options]

# Show filtered data
st.dataframe(filtered_df[display_cols].rename(columns=alias_mapping), use_container_width=True)