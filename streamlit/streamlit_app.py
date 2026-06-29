"""
# My first app
Here's our first attempt at using data to create a table:
"""

from datetime import datetime

import streamlit as st
import os
import ijson
from analysis_modules.author_affiliation import AuthorAnalyzer
from shared.models import Article


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

st.title(file_select.split("/")[-1].split(".")[0])
file_stats = os.stat(file_select)
st.write(f"File size: {round(file_stats.st_size / 1000)}KB")
st.write(f"Modified date: {datetime.fromtimestamp(file_stats.st_mtime)}")

st.altair_chart(analyzers["author"].chart())
