#!/usr/bin/env bash

version=$(
    curl -sX GET \
        "https://api.github.com/repos/mylar3/mylar3/releases/latest" |
        jq -r '.tag_name'
)
version="${version#v}"

printf "%s" "${version}"
