#!/bin/bash

sed 's/--compressed/-o post.html --compressed/g' curl.txt > download_post.sh
/bin/bash download_post.sh
python get_post_urls.py

i=0
for d in $(cat post_urls.txt); do
	sed "s@https://banking.ing.de/app/postbox.*'@$d'@g" curl.txt | sed "s/--compressed/-O  --compressed/g" > download_document.sh
	/bin/bash download_document.sh
	i=$((i+1))
done;

python parse_docs.py