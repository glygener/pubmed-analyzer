import pandas as pd
import altair as alt
import streamlit as st

from .base_module import BaseModule
from models import Article


class JournalPieChart(BaseModule):
    def __init__(self):
        self.journals: dict[str, dict[str, int]] = {}

    def process_article(self, article: Article):
        journal = article.journal
        year = article.pub_year
        if journal in self.journals.keys():
            self.journals[journal]["count"] += 1
        else:
            self.journals[journal] = {"count": 1, "year": year}

    def dataframe(_self):
        journals: dict[str, list[str | int]] = {
            "journals": [],
            "count": [],
        }
        for k, v in _self.journals.items():
            journals["journals"].append(k)
            journals["count"].append(v["count"])
        return pd.DataFrame(journals, columns=["journals", "count"]).sort_values(
            "count", ascending=False
        )

    def pie_chart(_self):
        df = _self.dataframe()
        legend = alt.Legend(labelLimit=10000)
        chart = (
            alt.Chart(df)
            .mark_arc()
            .encode(theta="count", color=alt.Color("journals", legend=legend))
        )
        st.altair_chart(chart, width="stretch")
