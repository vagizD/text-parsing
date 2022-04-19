# text-parsing
NLP script which finds uppercase and titlecase words.

### Usage
`python spacy-script.py <text.txt> <output.html>`
where 
* `<text.txt>` - path to the file which contains text to find token matches.
* `<output.html>` - path to the file to write results to (creates one if it does not exist, otherwise overwrites the contents).

This script uses built-in python modules and two open-source libraries - `spacy` and `bs4`. Both are being installed when running `spacy-script.py`
if they are not installed.
