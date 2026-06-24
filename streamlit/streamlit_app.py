"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import os
import ijson
from analysis_modules.author_affiliation import AuthorAnalyzer
from models import Article


@st.cache_data
def process_file(file: str):
    author_analyzer = AuthorAnalyzer()

    with open(file) as f:
        for article in ijson.items(f, "item"):
            author_analyzer.process_article(Article(**article))

    return {"author": author_analyzer}


files = []
for file in os.listdir("/data"):
    if file.endswith(".json"):
        files.append(file)

file_select = f"/data/{st.sidebar.selectbox("Choose a file for analysis:", files)}"


analyzers = process_file(file_select)

st.altair_chart(analyzers["author"].chart())
