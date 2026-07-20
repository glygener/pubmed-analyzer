from abc import ABC, abstractmethod
from models import Article


class BaseModule(ABC):
    """
    Base class for analysis module classes
    """

    @abstractmethod
    def process_article(self, article: Article):
        pass
