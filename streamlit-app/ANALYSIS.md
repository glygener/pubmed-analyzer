# Streamlit Analysis Dashboard
The Streamlit analysis dashboard is currently broken up into two pages. The data display App page and this About page. The App page displays various analysis visualizations that are generated via analysis modules in the `analysis_modules/` directory at the root of this app. 

## Analysis Modules
Analysis modules are implementations of the abstract `BaseModule` class which is defined in `analysis_modules/base_module.py`:
```
from abc import ABC, abstractmethod
from models import Article


class BaseModule(ABC):
    """
    Base class for analysis module classes
    """

    @abstractmethod
    def process_article(self, article: Article):
        pass
```
New analysis modules must subclass the `BaseModule` class and implement a `process_article(self, article: Article)` method. This method is called in `pages/0_App.py:15` in the `process_file` function:
```
@st.cache_data
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
```
When a new module class is made, create an instance of it in the above function with the other module instantiations and add it to the for loop and the return object of the function to be able to render the module's visualization methods from the analyzer at the end of `pages/0_App.py` like:
```
st.header("Author Attribute Completeness")
analyzers["author_affiliation"].chart()
st.header("Author Affiliation by Country")
analyzers["author_map"].map()
st.header("Mesh Terms")
analyzers["mesh_term_word_cloud"].word_cloud()
st.header("Journal Distribution")
analyzers["journal_pie_chart"].pie_chart()
```
Follow the example of the existing analysis modules to see how articles are processed and other visualizations are created. If a new module uses a python package that is not already in `requirements.txt`, be sure to add the package to the requirements document to ensure the docker image is built with the necessary dependencies.