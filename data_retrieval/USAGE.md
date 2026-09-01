# Search Script Usage
```
data_retrieval/search.sh [-r] [-o output_dir] search_term
```
Searches PubMed with a given search term an outputs the results to an XML file named after the search term
* -r: optional flag forces refresh of of the given search
* -o output_dir: optional arg specifies an output directory for the resulting xml file (default is pubmed-analyzer/data)
* search_term: the term to search PubMed for using EDirect