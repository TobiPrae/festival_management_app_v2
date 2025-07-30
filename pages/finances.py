import streamlit as st
import numpy as np
from utils.functions import get_json
import pandas as pd
from utils.functions import read_from_datastore
from utils.functions import require_login

require_login() 

st.set_page_config(page_title="Finanzen")
st.title("Finanzen")

variables = read_from_datastore("variables")[0]
todos = read_from_datastore("todos")
participants = read_from_datastore("participants")

# Convert to DataFrame
df_participants = pd.DataFrame(participants)
df_todos = pd.DataFrame(todos)

# Group by category and sum costs
summary = df_todos.groupby("category").agg({
    "estimated_cost": "sum",
    "actual_cost": "sum"
}).reset_index().sort_values(by=["actual_cost"], ascending=[ False])

summary_tasks = df_todos.groupby("task").agg({
    "estimated_cost": "sum",
    "actual_cost": "sum"
}).reset_index().sort_values(by=["actual_cost"], ascending=[ False])

# Compute total expenses
beverage_amount_paid = df_participants["beverage_amount_paid"].sum()
ticket_amount_paid = df_participants["ticket_amount_paid"].sum()
estimated_cost = df_todos["estimated_cost"].sum()
actual_cost = df_todos["actual_cost"].sum()
savings = variables["savings"]
donation = variables["donation"]
df_participants["beverage_amount_target"] = (df_participants["count_alcoholic_bewerages"] * variables['alcoholic_beverage_price']) + (df_participants["count_non_alcoholic_bewerages"] * variables['non_alcoholic_beverage_price']) + (df_participants["count_weisswurst"] * variables['weisswurst_price'])
df_participants["ticket_amount_target"] = np.where(df_participants["attending_days"] == "Both", variables['two_day_ticket'], variables['one_day_ticket']) 
beverage_amount_target = df_participants["beverage_amount_target"].sum()
ticket_amount_target = df_participants["ticket_amount_target"].sum()
estimated_costs = dict(zip(summary["category"], summary["estimated_cost"]))
actual_costs = dict(zip(summary["category"], summary["actual_cost"]))
estimated_costs_detail = dict(zip(summary_tasks["task"], summary_tasks["estimated_cost"]))
actual_costs_detail = dict(zip(summary_tasks["task"], summary_tasks["actual_cost"]))


# Sidebar filters
st.sidebar.header("Filteroptionen")

cost_options = ["Tatsächlich", "Geschätzt"]
selected_cost_options = st.sidebar.selectbox("Kostenkategorie", cost_options)

split_options = ["Grob", "Detail"]
selected_split_options = st.sidebar.selectbox("Aufschlüsselung", split_options)

if selected_cost_options == "Geschätzt":
    cost_dict = estimated_costs
    cost_dict_detail = estimated_costs_detail
    beverage_amount = beverage_amount_target
    ticket_amount = ticket_amount_target
    total_paid = beverage_amount_target + ticket_amount_target + savings
    total_cost = estimated_cost + donation

else:
    cost_dict = actual_costs
    cost_dict_detail = actual_costs_detail
    beverage_amount = beverage_amount_paid
    ticket_amount = ticket_amount_paid
    total_paid = beverage_amount_paid + ticket_amount_paid + savings
    total_cost = actual_cost + donation

diff = total_paid - total_cost

# Display results
left_col, right_col = st.columns(2)

with left_col:
    total_expenses = 0.0

    if selected_split_options == "Grob":
        for category in summary["category"]:
            cost = cost_dict.get(category, 0)
            total_expenses += cost
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(category)
            with col2:
                st.write(f"{cost:.2f} €")
    else:
        for task in summary_tasks["task"]:
            cost = cost_dict_detail.get(task, 0)
            total_expenses += cost
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(task)
            with col2:
                st.write(f"{cost:.2f} €")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("Spenden")
    with col2:
        st.write(f"{donation:.2f} €")
            
    if diff > 0:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(
                f"<span style='color: green;'>Gewinn</span>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<span style='color: green;'>{diff:.2f} €</span>",
                unsafe_allow_html=True
            )



with right_col:
    total_income = beverage_amount + ticket_amount
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Getränke und Weißwürste")
        st.write("Pauschale")
        st.write("Vorjahresgewinn")
    with col2:
        st.write(f"{beverage_amount:.2f} €")
        st.write(f"{ticket_amount:.2f} €")
        st.write(f"{savings:.2f} €")

    if diff < 0:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(
                f"<span style='color: red;'>Verlust</span>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<span style='color: red;'>{abs(diff):.2f} €</span>",
                unsafe_allow_html=True
            )


st.divider()
left_col_total, right_col_total = st.columns(2)
with left_col_total:
    col1, col2 = st.columns([2, 1])
    with col1:
            st.subheader(f"**Gesamt**")
    with col2:
        if diff > 0:
            st.subheader(f"**{total_paid:.2f} €**")
        else:
            st.subheader(f"**{total_cost:.2f} €**")
with right_col_total:
    col1, col2 = st.columns([2, 1])
    with col1:
            st.subheader(f"**Gesamt**")
    with col2:
        if diff < 0:
            st.subheader(f"**{total_cost:.2f} €**")
        else:
            st.subheader(f"**{total_paid:.2f} €**")
