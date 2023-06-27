#!/usr/bin/env python3

from semanticscholar import SemanticScholar
import tqdm
import yaml
import argparse

sch = SemanticScholar()

args = argparse.ArgumentParser()
args.add_argument(
    "-t", "--tsv-file",
    default="data/2022.acl-findings.cit2023.tsv"
)
args.add_argument("-y", "--yaml-file", default="tmp/papers_acl_2022.yml")
args = args.parse_args()

PREFIX = args.tsv_file.split("/")[-1]
FILE_TGT_SHORT = open(
    f"data/{PREFIX.replace('findings', 'findings-short').replace('main', 'main-short')}",
    "w"
)
FILE_TGT_LONG = open(
    f"data/{PREFIX.replace('findings', 'findings-long').replace('main', 'main-long')}",
    "w"
)

title_to_type = {
    x["title"].lower(): x["attributes"]["paper_type"]
    for x in yaml.safe_load(open(args.yaml_file, "r").read())
}

data = [
    tuple(x.rstrip("\n").split("\t"))
    for x in open(args.tsv_file, "r")
]

def get_title(doi):
    try:
        paper = sch.get_paper(doi)
        x = paper.title.lower()
        return x
    except Exception as e:
        print(e)
        return None


for doi_orig, cit in tqdm.tqdm(data):
    doi_acl = f"ACL:{doi_orig.split('/')[-1]}"
    # first try ACL DOI
    doi = doi_acl

    title = None
    attempts = 0
    while title is None:
        title = get_title(doi)
        attempts += 1
        if attempts >= 2 and title is None:
            print("Skipping", doi, "after 2 unsuccessful attempts")
            # try original DOI as fallback
            if doi != doi_orig:
                doi = doi_orig
                attempts = 0
            else:
                break

    if title is None or title not in title_to_type:
        print(f">{title}< not in title_to_type")
        continue
    if title_to_type[title] == "long paper":
        FILE_TGT_LONG.write(f"{doi_orig}\t{cit}\n")
    elif title_to_type[title] == "short paper":
        FILE_TGT_SHORT.write(f"{doi_orig}\t{cit}\n")
    else:
        print("Unknown paper type", title_to_type[title])
