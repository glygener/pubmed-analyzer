# Parse Script Usage
```
python -m data_normalization.parse [-h] [--csv] [-o, --output OUTPUT] file_path
```
parses a given PubMed results XML file into a JSON file, pulling out each article's pmid, title, publication month and year, journal name, and author information
* -h: show usage information
* --csv: optional flag tells the script to output a flat csv file with author information in addition to JSON output
* -o, --output OUTPUT: specify file to output results to.
* file_path: full path to the XML file to be parsed