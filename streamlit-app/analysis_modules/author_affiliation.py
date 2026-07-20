import altair as alt
import pandas as pd
import streamlit as st

from .base_module import BaseModule
from models import Article


class AuthorAffiliation(BaseModule):
    def __init__(self):
        self.total_authors: int = 0
        self.total_institutions: int = 0
        self.total_departments: int = 0
        self.total_cities_or_states: int = 0
        self.total_countries: int = 0

    def process_article(self, article: Article):
        for author in article.authors:
            self.total_authors += 1
            if author.institution:
                self.total_institutions += 1
            if author.department:
                self.total_departments += 1
            if author.city or author.state:
                self.total_cities_or_states += 1
            if author.country:
                self.total_countries += 1

    def dataframe(self):
        return pd.DataFrame(
            [
                {
                    "attribute": "Institution",
                    "present": self.total_institutions,
                    "missing": self.total_authors - self.total_institutions,
                },
                {
                    "attribute": "Department",
                    "present": self.total_departments,
                    "missing": self.total_authors - self.total_departments,
                },
                {
                    "attribute": "City/State",
                    "present": self.total_cities_or_states,
                    "missing": self.total_authors - self.total_cities_or_states,
                },
                {
                    "attribute": "Country",
                    "present": self.total_countries,
                    "missing": self.total_authors - self.total_countries,
                },
            ]
        )

    def chart(_self):
        df = _self.dataframe().melt(
            id_vars="attribute",
            value_vars=["present", "missing"],
            var_name="status",
            value_name="count",
        )
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("attribute:N", sort="-x", title="Author Attribute"),
                y=alt.Y(
                    "count:Q",
                    stack="normalize",
                    axis=alt.Axis(format="%"),
                    title="Authors",
                ),
                color=alt.Color(
                    "status:N",
                    scale=alt.Scale(
                        domain=["missing", "present"], range=["#d63b3b", "#0e26c0"]
                    ),
                    title="",
                ),
                tooltip=["attribute", "status", "count"],
            )
            .properties(height=550)
        )
        st.altair_chart(chart)
