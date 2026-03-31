from lxml import etree
import csv
import re

xml_file = "data/glycomics.xml"
output_file = "output/pubmed_authors.tsv"
country_csv = "data/countries.csv"

def load_countries(path):
    countries = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            countries.append(row["country"].strip())
    return countries

countries = load_countries(countries_csv)

parser = etree.XMLParser(recover=True)
tree = etree.parse(xml_file, parser)
root = tree.getroot()

def extract_country(affiliation):
    if not affiliation:
        return "Unknown"

    affiliation = re.sub(r'\S+@\S+', '', affiliation)
 
    affiliation = affiliation.replace(".", "")

    for country in countries:
        if country.lower() in affiliation.lower():
            return country

    parts = affiliation.split(",")
    if parts:
        return parts[-1].strip()

    return "Unknown"


with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter="\t")

    writer.writerow(["Author", "Country", "PMID"])

    for article in root.xpath("//PubmedArticle"):

        pmid = article.xpath(".//PMID/text()")
        if not pmid:
            continue
        pmid = pmid[0]

        for author in article.xpath(".//Author"):

            last = author.findtext("LastName")
            initials = author.findtext("Initials")

            if not last or not initials:
                continue

            author_name = f"{last} {initials}"

            affiliation = author.findtext(".//Affiliation")
            country = extract_country(affiliation)

            writer.writerow([author_name, country, pmid])

print(output_file)
