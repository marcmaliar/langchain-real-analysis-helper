#!/bin/bash

while IFS= read -r url; do
    # Extract the filename from the URL
    filename=$(basename "$url")
    # Use curl to perform the desired operation on each URL and save it to the data directory
    curl -o "./data/$filename" -O "$url"
    iconv -f ISO-8859-1 -t UTF-8 "./data/$filename" > "./data/${filename}.utf8"
done < urls.txt