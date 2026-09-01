from abc import ABC, abstractmethod
from models import Article

import streamlit as st


class BaseModule(ABC):
    """
    Base class for analysis module classes
    """

    @st.cache_data
    @abstractmethod
    def process_article(self, article: Article):
        pass
