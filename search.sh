#!/usr/bin/env bash

set -euo pipefail

usage() {
    echo "Usage: $0 [-r] SEARCH_TERM"
    exit 1
}

refresh=false
search_parts=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -r)
            refresh=true
            shift
            ;;
        *)
            search_parts+=("$1")
            shift
            ;;
    esac
done

if [[ ${#search_parts[@]} -eq 0 ]]; then
    usage
fi

search_term="${search_parts[*]}"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
data_dir="$script_dir/data"
mkdir -p "$data_dir"

file_name="$(echo "$search_term" | tr '[:upper:]' '[:lower:]' | sed 's/ /_/g').xml"
file_path="$data_dir/$file_name"

if [[ "$refresh" == false && -f "$file_path" ]]; then
    mod_time=$(stat -c %y "$file_path" 2>/dev/null || stat -f "%Sm" "$file_path")
    echo "The search term '$search_term' was previously used at $mod_time and the results are saved at $file_path."
    echo "Use -r flag to overwrite the file."
    exit 0
fi

echo "Running PubMed query..."
echo "Search term: $search_term"

esearch -db pubmed -query "$search_term" | efetch -format xml > "$file_path"

echo "Saved results to $file_path"