# PubMed Analyzer
## Requirements
* [EDirect](#edirect)
* [Docker](https://docs.docker.com/engine/install/)
## Usage
This project contains scripts and tooling for PubMed data querying and analysis.

### Streamlit (WIP)
The streamlit app in `streamlit/` analyzes JSON data produced by the parsing script and visualizes them in the browser.

* Run `docker compose up` in the repository root to bring up the streamlit app in a docker container. Once the container initializes, navigate to http://localhost:8501 in your browser to see the frontend. The docker container mounts the `data/` directory in the repository and the streamlit app scans the mounted directory for `.json` files to analyze.

### Data Scripts
* `data_scripts/search.sh [-r] [-o output_dir] search_term` Searches pubmed with a given search term an outputs the results to an XML file named after the search term
   * -r: optional flag forces refresh of of the given search
   * -o output_dir: optional arg specifies an output directory for the resulting xml file (default is pubmed-analyzer/data)
   * search_term: the term to search PubMed for using EDirect

* `python -m data_scripts.parse [-h] [--csv] [-o, --output OUTPUT] file_path` parses a given PubMed results XML file into a JSON file, pulling out each article's pmid, title, publication month and year, journal name, and author information

   * -h: show usage information
   * --csv: optional flag tells the script to output a flat csv file with author information in addition to JSON output
   * -o, --output OUTPUT: specify file to output results to.
   * file_path: full path to the XML file to be parsed
      
## <a name="edirect"></a>EDirect Installation Instructions
* Open a terminal window and run one of the following commands to download and install the software:

    * sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"
    * sh -c "$(wget -q https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"

This will prompt a number of script downloads that will be compiled into an "edirect" folder in the user's home directory

You may update the PATH environment variable in the user's configuration file:
* echo "export PATH=\$HOME/edirect:\$PATH" >> $HOME/.bash_profile

Answer "y" and press the Return key if you want to run the PATH update command 

* If the PATH is already set or want to make editing changes manually, press Return
* Once installation is complete, run line below to set the PATH for the current terminal session
    * export PATH=${HOME}/edirect:${PATH}

## PubMed Keyword PMID List
* Run the following command line below:
   * esearch -db pubmed -query "your keyword or search terms" | efetch -format uid

The command line will take the keyword or search terms and search the PubMed database to retrieve the records identified by the piped information and format the output into a simple list of unique identifiers

* In order to save the list of PMIDs to a file type (recommend XML), utilize a redirection operator to the mentioned command line
   * esearch -db pubmed -query "your keyword or search terms" | efetch -format uid > file_name

This step was done to ensure that all PMIDs for the corresponding keyword appeared. 

## PubMed Keyword XML File 
* Run the following command line below:
   * esearch -db pubmed -query "your keyword or search terms" | efetch -format xml > file_name

## PubMed Keyword PMID, Authors, Affiliations, and Journal List
* Use the XML file created from the previous step to extract only the PMID, authors, affiliations, and journal list
   * xtract -input "file name" -pattern PubmedArticle -element MedlineCitation/PMID -block Author -pfx "\n" -element LastName,Initials,AffiliationInfo/Affiliation -sep "\n" > file_name

