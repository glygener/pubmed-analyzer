from wordcloud import WordCloud  # type: ignore
import pandas as pd
import streamlit as st

from .base_module import BaseModule
from models import Article

SPECIAL_CASES = {"XKX": "Kosovo"}


class MeshTermWordCloud(BaseModule):
    def __init__(self):
        self.mesh_terms: list[dict[str, str | int]] = []

    def process_article(self, article: Article):
        if article.mesh_terms:
            for term in article.mesh_terms:
                self.mesh_terms.append({"term": term.term, "year": article.pub_year})

    def dataframe(_self):
        df = pd.DataFrame(_self.mesh_terms, columns=["year", "term"])
        return df

    def word_cloud(_self):
        df = _self.dataframe().copy()

        # Count term frequencies
        freq = df["term"].value_counts()

        min_freq, max_freq = st.slider(
            "Word frequency range",
            int(freq.min()),
            int(freq.max()),
            (int(freq.min()), int(freq.max())),
        )

        # Keep only terms within the selected frequency range
        filtered_freq = freq[freq.between(min_freq, max_freq)]

        st.dataframe(freq, height=200)

        wc = WordCloud(  # type: ignore
            width=2000,
            height=1000,
            background_color="white",
            colormap="viridis",
        )

        wc.generate_from_frequencies(filtered_freq)  # type: ignore

        st.image(wc.to_array(), width="stretch")  # type: ignore
