import streamlit as st



st.set_page_config(
    page_title="KZF Orga",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = {
    "Home" :[
        st.Page("pages/landing.py", title="🏠 Home"),
    ],
    "Organisatorisches" :[
        st.Page("pages/planning.py", title="✅ Planung"),
        st.Page("pages/settings.py", title="⚙️ Einstellungen"),
    ],
    "Finanzen"  :[
        st.Page("pages/finances.py", title="📊 Übersicht"),
        st.Page("pages/expenses.py", title="💸 Ausgaben"),
    ],
    "Teilnehmer" :[
        st.Page("pages/participants_overview.py", title="📋 Übersicht"),
        st.Page("pages/participants_edit.py", title="✏️ Bearbeiten"),
        st.Page("pages/participants_add_multiple.py", title="➕ Hinzufügen"),
    ]
}

pg = st.navigation(pages)
pg.run()


