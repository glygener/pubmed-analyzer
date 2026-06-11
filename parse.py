#!/usr/bin/env python3
from pathlib import Path
from pprint import pprint
import sys

from argparse import ArgumentParser
from typing import Optional
from lxml import etree
from lxml.etree import _Element  # type: ignore
import pycountry
from gliner import GLiNER

from pydantic import BaseModel

parser = ArgumentParser()
parser.add_argument(
    "filename",
    type=str,
    help="File name to run analysis on.",
)
args = parser.parse_args()


class Author(BaseModel):
    name: str
    department: Optional[str] = None
    institution: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class MeshTerm(BaseModel):
    term: str
    ui: str
    major_topic: bool


class Article(BaseModel):
    pmid: str
    title: str
    pub_year: int
    pub_month: Optional[str] = None
    journal: str
    authors: list[Author]
    mesh_terms: Optional[list[MeshTerm]] = []


# Initialize gliner
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
labels = ["department", "institution", "city", "country"]

# Static list of countries for matching afiliations
COUNTRIES = {c.name.lower(): c.name for c in pycountry.countries}
# Add common variants
COUNTRIES.update(
    {
        "usa": "United States",
        "u.s.a.": "United States",
        "uk": "United Kingdom",
        "u.k.": "United Kingdom",
        "united states of america": "United States",
    }
)


def get_required_text(element: _Element, xpath: str) -> str:
    text = element.findtext(xpath)

    if not text:
        raise ValueError(
            f"Expected element value missing: {xpath}\nElement:\n{etree.tostring(element, pretty_print=True)}"
        )
    return text.strip()


def get_affiliation_info(text: str | None) -> dict[str, str | None]:
    if text:
        entities = model.predict_entities(text, labels)
        department = institution = city = country = None

        for entity in entities:
            match entity["label"]:
                case "department":
                    department = entity["text"]
                case "institution":
                    institution = entity["text"]
                case "city":
                    if city:
                        city = f"{city}, {entity['text']}"
                    else:
                        city = entity["text"]
                case "country":
                    country = entity["text"]
                    if country in COUNTRIES.keys():
                        country = COUNTRIES[country]
                case _:
                    continue

        return {
            "department": department,
            "institution": institution,
            "city": city,
            "country": country,
        }
    return {}


def parse_authors(authors: list[_Element]) -> list[Author]:
    author_list: list[Author] = []
    for author in authors:
        name = f"{get_required_text(author, ".//ForeName")} {get_required_text(author, ".//LastName")}"
        affiliation = get_affiliation_info(author.findtext(".//Affiliation"))
        author_list.append(Author(name=name, **affiliation))
    return author_list


def parse_mesh_terms(descriptors: list[_Element]) -> list[MeshTerm]:
    mesh_term_models: list[MeshTerm] = []
    for d in descriptors:
        mesh_term = MeshTerm(
            term=(d.text or "").strip(),
            ui=d.get("UI") or "",
            major_topic=d.get("MajorTopicYN") == "Y",
        )
        mesh_term_models.append(mesh_term)

    return mesh_term_models


def parse_article(article: _Element) -> Article:
    pmid = get_required_text(article, ".//PMID")
    title = get_required_text(article, ".//ArticleTitle")

    pub_year_text = get_required_text(article, ".//Journal//Year")
    pub_month = article.findtext(".//Journal//Month")

    journal = get_required_text(article, ".//Journal//Title")

    authors = parse_authors(article.findall(".//Author"))

    mesh_terms = parse_mesh_terms(
        article.findall(".//MeshHeadingList/MeshHeading/DescriptorName")
    )

    return Article(
        pmid=pmid,
        title=title,
        pub_year=int(pub_year_text),
        pub_month=pub_month,
        journal=journal,
        authors=authors,
        mesh_terms=mesh_terms,
    )


def main():
    # Gather args and file path for reading
    filename: str = args.filename
    data_dir = Path(__file__).parent / "data"
    file_path = data_dir / f"{filename.lower().replace(' ', '_')}.xml"

    if not file_path.exists():
        print(f"The file {file_path} cannot be found")
        return

    with open(file_path, "rb") as f:
        results: list[Article] = []
        for _, article in etree.iterparse(f, tag="PubmedArticle"):
            results.append(parse_article(article))
            article.clear(keep_tail=True)

    for a in results:
        print(a.model_dump_json(indent=2))


if __name__ == "__main__":
    sys.exit(main())
