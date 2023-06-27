#!/usr/bin/env python3

DOIS_END = [
    "10.18653/v1/2021.acl-long.571",
    "10.18653/v1/2021.acl-short.139",
    "10.18653/v1/2021.findings-acl.457",
    "10.18653/v1/2022.acl-long.603",
    "10.18653/v1/2022.acl-short.97",
    "10.18653/v1/2022.findings-acl.331",

    "10.18653/v1/2023.eacl-main.280",
    "10.18653/v1/2023.findings-eacl.197",
    "10.18653/v1/2022.naacl-main.442",
    "10.18653/v1/2022.findings-naacl.209",

    "10.18653/v1/2020.emnlp-main.752",
    "10.18653/v1/2020.findings-emnlp.443",
    "10.18653/v1/2021.emnlp-main.847",
    "10.18653/v1/2021.findings-emnlp.424",
    "10.18653/v1/2022.emnlp-main.828",
    "10.18653/v1/2022.findings-emnlp.547",
]

# ./src/get_citations.py -p 2021.acl-long
# ./src/get_citations.py -p 2021.acl-short
# ./src/get_citations.py -p 2021.acl-findings
# ./src/get_citations.py -p 2022.acl-long
# ./src/get_citations.py -p 2022.acl-short
# ./src/get_citations.py -p 2022.acl-findings

# ./src/get_citations.py -p 2023.eacl-main
# ./src/get_citations.py -p 2023.eacl-findings
# ./src/get_citations.py -p 2022.naacl-main
# ./src/get_citations.py -p 2022.naacl-findings

# ./src/get_citations.py -p 2020.emnlp-main
# ./src/get_citations.py -p 2020.emnlp-findings
# ./src/get_citations.py -p 2021.emnlp-main
# ./src/get_citations.py -p 2021.emnlp-findings
# ./src/get_citations.py -p 2022.emnlp-main
# ./src/get_citations.py -p 2022.emnlp-findings

for DOI_END in DOIS_END:
    end = int(DOI_END.split(".")[-1])
    PREFIX = ".".join(DOI_END.split(".")[:-1])
    FNAME = ".".join(DOI_END.split("/")[-1].split(".")[:-1])
    FNAME = f"data/DOIs/{FNAME}.tsv"
    if "findings-" in FNAME:
        FNAME = FNAME.replace("findings-", "").replace(".tsv", "-findings.tsv")
    if "-long" in FNAME:
        FNAME = FNAME.replace("-long", "-main-long")
    if "-short" in FNAME:
        FNAME = FNAME.replace("-short", "-main-short")
    f = open(FNAME, "w")
    f.write("DOI\n")

    for i in range(1, end + 1):
        f.write(f"{PREFIX}.{i}\n")
