# PubMed Analyzer
## Requirements
* [EDirect](#edirect)
* [Docker](https://docs.docker.com/engine/install/)
* [make](https://www.gnu.org/software/make/)
## Usage
This project contains scripts and tooling for PubMed data querying and analysis.

### Makefile
The easiest way to use the available commands in the `Makefile` from the root of the directory:

```
make search SEARCH_INPUT="example"
```
* Searches PudMed for a given search term. `SEARCH_INPUT` should be valid input for the [search script](#search) wrapped in double quotes.
* Note: To make a search using the script options and a query with spaces, wrap the query in single quotes inside the double quotes. For example: `make search SEARCH_INPUT="-o ~/my-data 'term_1 AND term_2'"` queries PubMed with the query string "term_1 AND term_2" and creates a new file at `./my-data/term_1_and_term_2.xml`.


```
make parse PARSE_INPUT="example"
```
* Parses a given XML file into a JSONL file for analysis. `PARSE_INPUT` should be valid input for the [parse script](#parse) wrapped in double quotes.

```
make pull [TAG="latest"]
```
* Pull the latest `glygen/pubmed-analyzer` image by default.
* Optionally set the `TAG` variable to pull an image with a specific version tag.

```make run [DATA_DIRECTORY="./data/"] [TAG="latest"]```
* Run `make run` to start the pubmed-analysis Streamlit app in a docker container using the `glygen/pubmed-analyzer:latest` image by default and `./data/` as the default data mount for the container.
* Optionally set the `DATA_DIRECTORY` variable to point to a different directory with your JSONL data to be analyzed.
* Optionally set the `TAG` variable to run a container with a specific version tag.

```
make run-dev
```
* Run the pubmed-analysis Streamlit app using docker compose for development. See the (docker compose)[compose] section for more.

```
make build [TAG="latest"]
```
* Build an image tagged as `glygen/pubmed-analyzer:latest` by default.
* Optionally set the `TAG` variable to build an image with a specific version tag.

```
make push [TAG="latest"]
```
* Push an image to the glygen repository tagged as `glygen/pubmed-analyzer:latest` by default.
* Optionally set the `TAG` variable to push an image with a specific version tag.

```
make build push [TAG="latest"]
```
* One line command to build and push an image to the glygen repository tagged as `glygen/pubmed-analyzer:latest` by default.
* Optionally set the `TAG` variable to build and push an image with a specific version tag.

### Streamlit
The streamlit app in `streamlit/` analyzes JSONL files produced by the parsing script and visualizes them in the browser. To run the app, do one of the following:

* <a name="compose"></a>(docker compose) Run `docker compose up` in the repository root to bring up the streamlit app in a docker container. Once the container initializes, navigate to http://localhost:8501 in your browser to see the frontend. The docker container mounts the `./data/` directory in the repository and the streamlit app scans the mounted directory for `.jsonl` files to analyze. The `streamlit-app/` is also mounted to the container to allow for hot reloading while developing the Streamlit dashboard.

* (docker) Pull the image from glygen/pubmed-analyzer via `docker pull glygen/pubmed-analyzer` to pull the latest image. Run the container via `docker run -v {YOUR_DATA_DIRECTORY}:/data -p 8501:8501 pubmed-analyzer` to start the container. Once the container initializes, navigate to http://localhost:8501 in your browser to see the frontend. The streamlit app scans the mounted data directory for `.jsonl` files to analyze. Alternatively, you may build the image from scratch via `cd streamlit-app/ && docker build -t pubmed-analyzer .` and then run it as described above.


### Data Scripts
<a name="search"></a>
```
data_scripts/search.sh [-r] [-o output_dir] search_term
```
Searches PubMed with a given search term an outputs the results to an XML file named after the search term
* -r: optional flag forces refresh of of the given search
* -o output_dir: optional arg specifies an output directory for the resulting xml file (default is pubmed-analyzer/data)
* search_term: the term to search PubMed for using EDirect

<a name="parse"></a>
```
python -m data_scripts.parse [-h] [--csv] [-o, --output OUTPUT] file_path
```
parses a given PubMed results XML file into a JSON file, pulling out each article's pmid, title, publication month and year, journal name, and author information
* -h: show usage information
* --csv: optional flag tells the script to output a flat csv file with author information in addition to JSON output
* -o, --output OUTPUT: specify file to output results to.
* file_path: full path to the XML file to be parsed
      
## <a name="edirect"></a>EDirect Installation Instructions
Open a terminal window and run one of the following commands to download and install the software:

```
sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
```
```
sh -c "$(wget -q https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"
```

This will prompt a number of script downloads that will be compiled into an "edirect" folder in the user's home directory

You may update the PATH environment variable in the user's configuration file:
`echo "export PATH=\$HOME/edirect:\$PATH" >> $HOME/.bash_profile`

Answer "y" and press the Return key if you want to run the PATH update command 

* If the PATH is already set or want to make editing changes manually, press Return
* Once installation is complete, run `export PATH=${HOME}/edirect:${PATH} ` to set the PATH for the current terminal session


## PubMed Keyword PMID List
Input a keyword or search terms and search the PubMed database to retrieve the records identified by the piped information and format the output into a simple list of unique identifiers
```
esearch -db pubmed -query "your keyword or search terms" | efetch -format uid
```

In order to save the list of PMIDs to a file type (recommend XML), utilize a redirection operator to the mentioned command line
```
esearch -db pubmed -query "your keyword or search terms" | efetch -format uid > file_name
```

This step is done to ensure that all PMIDs for the corresponding query appeared.

## PubMed Keyword XML File 
Run the following command below to create an XML file of the PubMed query results:
```
esearch -db pubmed -query "your keyword or search terms" | efetch -format xml > file_name
```

## PubMed Keyword PMID, Authors, Affiliations, and Journal List
Use the XML file created from the previous step to extract only the PMID, authors, affiliations, and journal list
```
xtract -input "file name" -pattern PubmedArticle -element MedlineCitation/PMID -block Author -pfx "\n" -element LastName,Initials,AffiliationInfo/Affiliation -sep "\n" > file_name
```

