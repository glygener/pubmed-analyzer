import pandas as pd
import streamlit as st
import plotly.express as px  # type: ignore
import pycountry

from .base_module import BaseModule
from models import Article

SPECIAL_CASES = {"XKX": "Kosovo"}


class AuthorMap(BaseModule):
    def __init__(self):
        self.unique_authors: set[tuple[str, str | None]] = set()
        self.countries: dict[str, int] = {}
        self.first_countries: dict[str, int] = {}
        self.last_countries: dict[str, int] = {}

    def process_article(self, article: Article):
        if len(article.authors) > 0:
            # first author
            self._process_country(article.authors[0].country, self.first_countries)
            # last author
            self._process_country(article.authors[-1].country, self.last_countries)
            for author in article.authors:
                key = (author.name, author.affiliation_text)
                if key not in self.unique_authors:
                    self._process_country(author.country, self.countries)
                    self.unique_authors.add(key)

    @staticmethod
    def _process_country(country: str | None, countries: dict[str, int]):
        if country:
            if country not in countries.keys():
                countries[country] = 1
            else:
                countries[country] += 1

    def dataframe(self, first_or_last: bool | None = None):
        country_dict: dict[str, list[str | int]] = {
            "country": [],
            "count": [],
            "country_name": [],
        }

        if first_or_last is None:
            countries = self.countries
        elif first_or_last:
            countries = self.first_countries
        else:
            countries = self.last_countries

        for c, v in countries.items():
            country_dict["country"].append(c)
            country_dict["count"].append(v)
            try:
                country_dict["country_name"].append(pycountry.countries.lookup(c).name)
            except LookupError:
                country_dict["country_name"].append(SPECIAL_CASES.get(c) or "")
        return pd.DataFrame(country_dict, columns=["country", "count", "country_name"])

    def map(_self, first_or_last: bool | None = None):
        first_or_last = st.selectbox(
            "Filter authors:",
            options=[None, True, False],
            format_func=lambda x: {
                None: "All Authors",
                True: "First Authors",
                False: "Last Authors",
            }[x],
        )

        df = _self.dataframe(first_or_last)
        map = px.choropleth(  # type: ignore
            df,
            locations="country",
            locationmode="ISO-3",
            color="count",
            color_continuous_scale="Viridis",
            hover_name="country_name",
            custom_data=["count"],
        )
        map.update_traces(  # type: ignore
            hovertemplate="<b>%{hovertext}</b><br>Authors: %{customdata[0]}",
        )
        map.update_geos(  # type: ignore
            showcoastlines=True,
            coastlinecolor="gray",
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="lightblue",
            showcountries=True,
            countrycolor="white",
            projection_type="equirectangular",
        )

        st.plotly_chart(map)
