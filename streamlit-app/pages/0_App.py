from datetime import datetime
import json
from typing import Any

import streamlit as st
import os
from analysis_modules.author_affiliation import AuthorAffiliation
from analysis_modules.author_map import AuthorMap
from analysis_modules.mesh_term_word_cloud import MeshTermWordCloud
from analysis_modules.journal_pie_chart import JournalPieChart
from models import Article


def process_file(file: str) -> dict[str, Any]:
    author_affiliation = AuthorAffiliation()
    author_map = AuthorMap()
    mesh_term_word_cloud = MeshTermWordCloud()
    journal_pie_chart = JournalPieChart()

    with open(file) as f:
        for article in f:
            article_obj = Article(**json.loads(article))
            author_affiliation.process_article(article_obj)
            author_map.process_article(article_obj)
            mesh_term_word_cloud.process_article(article_obj)
            journal_pie_chart.process_article(article_obj)

    return {
        "author_affiliation": author_affiliation,
        "author_map": author_map,
        "mesh_term_word_cloud": mesh_term_word_cloud,
        "journal_pie_chart": journal_pie_chart,
    }


files: list[str] = []
for file in os.listdir("/data"):
    if file.endswith(".jsonl"):
        files.append(file)

file_select = f"/data/{st.sidebar.selectbox("Choose a file for analysis:", files)}"


analyzers = process_file(file_select)

st.title(file_select.split("/")[-1].split(".")[0])
file_stats = os.stat(file_select)
st.write(f"File size: {round(file_stats.st_size / 1000)}KB")
st.write(f"Modified date: {datetime.fromtimestamp(file_stats.st_mtime)}")

st.header("Author Attribute Completeness")
analyzers["author_affiliation"].chart()
st.header("Author Affiliation by Country")
analyzers["author_map"].map()
st.header("Mesh Terms")
analyzers["mesh_term_word_cloud"].word_cloud()
st.header("Journal Distribution")
analyzers["journal_pie_chart"].pie_chart()
