from google.cloud import datastore
import streamlit as st

# Initialize the client
service_account_info = dict(st.secrets["service_account_key"])
client = datastore.Client.from_service_account_info(service_account_info)

kind = "participants"
property_to_remove = "paid_expenses"

# Query all entities of the kind
query = client.query(kind=kind)
entities = list(query.fetch())

# Remove the property and update the entity
for entity in entities:
    if property_to_remove in entity:
        del entity[property_to_remove]
        client.put(entity)

print(f"Removed '{property_to_remove}' from {len(entities)} entities.")
