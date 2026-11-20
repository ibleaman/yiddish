#!/usr/bin/env bash
# Fetch the data repos that yiddish/yiddish.py reads (the loshn-koydesh word
# lists and the Hasidic lexicon) into yiddish/submodules/, at the exact
# versions listed in data-versions.txt
#
# The GitHub Action runs this before building a release.
# To work on the package locally, run it once from the repo folder:
#     bash fetch_data.sh
set -euo pipefail
cd "$(dirname "$0")"

while read -r repo ref; do
  # skip blank lines and comments
  [[ -z "$repo" || "$repo" == \#* ]] && continue

  name="${repo##*/}"   # e.g., ibleaman/hasidify_lexicon -> hasidify_lexicon
  dest="yiddish/submodules/$name"
  rm -rf "$dest"
  mkdir -p "$dest"
  git init -q "$dest"
  git -C "$dest" fetch -q --depth 1 "https://github.com/$repo.git" "$ref"
  git -C "$dest" checkout -q FETCH_HEAD
  echo "$repo @ $(git -C "$dest" rev-parse --short HEAD) ($ref)"
done < data-versions.txt
