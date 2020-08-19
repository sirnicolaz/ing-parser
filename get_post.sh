#!/bin/bash

sed "s/\\\u0021/\!/g" curl.txt > curl_escaped.txt
sed 's/--compressed/-o post.html --compressed/g' curl_escaped.txt > download_post.sh
/bin/bash download_post.sh
python get_post_urls.py

i=0
for d in $(cat post_urls.txt); do
	sed "s@https://banking.ing.de/app/postbox.*'@$d'@g" curl_escaped.txt | sed "s/--compressed/-o post\/$i.pdf  --compressed/g" > download_document.sh
	/bin/bash download_document.sh
	i=$((i+1))
done;

python parse_docs.py

rm download_document.sh download_post.sh post_urls.txt curl_escaped.txt