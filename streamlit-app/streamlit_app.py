import streamlit as st

app = st.Page("pages/0_App.py", title="App")
about = st.Page("pages/1_About.py", title="About")

pg = st.navigation([app, about])
pg.run()
