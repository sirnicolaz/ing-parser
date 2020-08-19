# ing-parser
## Requirements
* Python 3.5+
* Pip
* virtualenv
## Setup
```
git clone git@github.com:sirnicolaz/ing-parser.git
cd ing-parser
mkdir venv
virtual venv
source venv/bin/activate
pip install -r requirements.txt
```
Or, if you don't have virtual env
```
git clone git@github.com:sirnicolaz/ing-parser.git
cd ing-parser
pip install -r requirements.txt
```
## Instructions
* Access your ING account
* Open the inspector, on the network tab
* Access the Post box page
* Select the page request, right click and "Copy as cURL"
* Paste the content inside a file named `curl.txt`
* Execute `sh get_post.sh`
* You will find a summary inside summary.tsv 
