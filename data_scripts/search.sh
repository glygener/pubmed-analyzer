#!/usr/bin/env bash

set -euo pipefail

usage() {
    echo "Usage: $0 [-r] [-o output_dir] search_term"
    exit 1
}

refresh=false
output_dir=""
search_parts=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -r)
            refresh=true
            shift
            ;;
        -o)
            [[ $# -lt 2 ]] && usage
            output_dir="$2"
            shift 2
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
repo_root="$(cd "$script_dir/.." && pwd)"

if [[ -z "$output_dir" ]]; then
    data_dir="$repo_root/data"
else
    data_dir="$output_dir"
fi

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

esearch -db pubmed -query "$search_term" | efetch -format xml | | sed -e 's/&alpha;/α/g' -e 's/&beta;/β/g' -e 's/&gamma;/γ/g' > "$file_path"

echo "Saved results to $file_path"