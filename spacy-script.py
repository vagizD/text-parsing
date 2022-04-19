import subprocess
import sys
import logging
import re

logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO,
    filename='logs.txt',
    filemode="w")

try:

    def install(package):
        output = subprocess.check_output(["pip", "freeze"]).decode('utf-8')
        output = re.findall(fr'\b{package}\b', output)
        if package not in output:
            logger.warning(f"Required package {package} is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            logger.info(f"{package} installed.")
        else:
            logger.info(f"Required package {package} already installed.")


    def download(data):
        logger.info(f"Downloading {data} for spaCy operations...")
        subprocess.check_output([sys.executable, "-m", "spacy", "download", data])
        logger.info(f"{data} downloaded.")

    # ensuring needed libraries are installed
    install("spacy")
    install("bs4")
    download("en_core_web_sm")

    # using spacy to find features
    import spacy
    from spacy.matcher import Matcher
    from collections import defaultdict

    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    upper = [{"IS_UPPER": True}]
    title = [{"IS_TITLE": True}]
    matcher.add("uppers", [upper])
    matcher.add("titles", [title])

    # reading text file
    filename = sys.argv[1]
    logger.info(f"Reading {filename}.")
    with open(filename, "r") as file:
        content = file.read()

    doc = nlp(content)
    matches = matcher(doc)

    # results
    matches_dict = {"uppers": defaultdict(list),
                    "titles": defaultdict(list)}

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        matches_dict[string_id][span.text].append(1)

    logger.info("Matches completed.")


    def results(dic):
        spaces = "--------"
        ind = "    "
        print(spaces)
        for key in dic.keys():
            print(f"{key}: ")
            for key1 in dic[key].keys():
                print(ind + f"{key1}: {len(dic[key][key1])}")
            print(spaces)


    def to_html(dic):
        html = ""
        for key in dic.keys():
            html += "<td>" + key + "</td>"
            for key1 in dic[key].keys():
                html += "<td>" + key1 + "</td>"
            html += "<tr>"

        html = "<table border=1>" + html + "</table"
        return html


    html = to_html(matches_dict)
    from bs4 import BeautifulSoup as bs

    soup = bs(html, 'lxml')
    aligned = soup.prettify()

    # writing to file
    output_file = sys.argv[2]
    logger.info(f"Writing results to {output_file}.")
    with open(output_file, "w") as file:
        file.write(aligned)

    logger.info(f"Script finished.")
    results(matches_dict)

except Exception:
    logger.critical("Script error occurred.")
    print("Script error occurred.")
