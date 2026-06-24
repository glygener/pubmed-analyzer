#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from pprint import pprint
import sys

from argparse import ArgumentParser
from lxml import etree
from lxml.etree import _Element  # type: ignore
import pycountry
from gliner2 import GLiNER2

from streamlit.models import Author, MeshTerm, Article

parser = ArgumentParser()
parser.add_argument(
    "file_path",
    type=str,
    help="Full XML file path to run analysis on.",
)
parser.add_argument(
    "--csv",
    action="store_true",
    help="Write parsed data to csv.",
)
parser.add_argument(
    "-o",
    "--output",
    help="Specify file to output results to.",
)
args = parser.parse_args()


# Initialize gliner
extractor = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
schema = extractor.create_schema().entities(
    {
        "institution": "A university, reasearch center, or institution where research happens",
        "department": "Department within an research institution",
        "city": {
            "description": "The city where an institution may reside",
            "threshold": 0.8,
        },
        "state": "The state where the city of the institution exists",
        "country": "The country where an institution resides",
    },
)

# Static list of countries for matching affiliations
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
    results: dict[str, str | None] = {
        "institution": None,
        "department": None,
        "city": None,
        "state": None,
        "country": None,
    }
    if text:
        entities = extractor.extract(text, schema, include_confidence=True)["entities"]

        for label in entities:
            top = 0
            for entity in entities[label]:
                if entity["confidence"] > top:
                    top = entity["confidence"]
                    results[label] = entity["text"]

    return results


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


def parse_article(article: _Element, csv_file_path: Path) -> Article:
    pmid = get_required_text(article, ".//PMID")
    title = get_required_text(article, ".//ArticleTitle")

    pub_year_text = get_required_text(article, ".//Journal//Year")
    pub_month = article.findtext(".//Journal//Month")

    journal = get_required_text(article, ".//Journal//Title")

    authors = parse_authors(article.findall(".//Author"))

    mesh_terms = parse_mesh_terms(
        article.findall(".//MeshHeadingList/MeshHeading/DescriptorName")
    )

    # Check for csv output option
    if args.csv:
        with open(csv_file_path, "a", newline="") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=[
                    "pmid",
                    "name",
                    "department",
                    "institution",
                    "city",
                    "country",
                ],
            )
            for author in authors:
                writer.writerow(
                    {
                        "pmid": pmid,
                        "name": author.name,
                        "department": author.department,
                        "institution": author.institution,
                        "city": author.city,
                        "country": author.country,
                    }
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
    file_path = Path(args.file_path)

    # Check for file
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path.__str__()} cannot be found")

    # Output file
    if args.output:
        output_path = Path(args.output)
        output_file_string = f"{output_path.parent}/{output_path.stem}"
    else:
        output_file_string = f"{file_path.parent}/{file_path.stem}"

    # Clear csv file if needed
    csv_file_path = Path(f"{output_file_string}.csv")
    if args.csv:
        with open(csv_file_path, "w", newline="") as csvfile:
            field_names = [
                "pmid",
                "name",
                "department",
                "institution",
                "city",
                "country",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

    try:
        with open(file_path, "rb") as f:
            results: list[Article] = []
            for _, article in etree.iterparse(f, tag="PubmedArticle"):
                results.append(parse_article(article, csv_file_path))
                article.clear(keep_tail=True)
    except etree.XMLSyntaxError as e:
        raise etree.XMLSyntaxError(
            f"Invalid XML file: {file_path.__str__()}", e.error_log
        )

    # Write results to JSON
    json_file_path = Path(f"{output_file_string}.json")
    with open(json_file_path, "w") as f:
        json.dump(([a.model_dump() for a in results]), f)


if __name__ == "__main__":
    sys.exit(main())
