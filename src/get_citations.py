#!/usr/bin/env python3

from semanticscholar import SemanticScholar
import csv
import tqdm
import os
import argparse

sch = SemanticScholar()

args = argparse.ArgumentParser()
args.add_argument("-p", "--prefix", default="2020.emnlp-findings")
args = args.parse_args()

FILE_SRC = f"data/DOIs/{args.prefix}.tsv"
FILE_TGT = f"data/{args.prefix}.cit2023.tsv"

data = [x["DOI"] for x in csv.DictReader(open(FILE_SRC, "r"), delimiter="\t")]

def get_citations(doi):
    try:
        paper = sch.get_paper(doi)
        x = paper.citationCount
        return x
    except Exception as e:
        print(e)
        return None

if os.path.exists(FILE_TGT):
    data_new = [tuple(x.strip("\n").split("\t")) for x in open(FILE_TGT, "r")]
    data = data[len(data_new):]
else:
    data_new = []

for doi_orig in tqdm.tqdm(data):
    doi_acl = f"ACL:{doi_orig.split('/')[-1]}"
    # first try ACL DOI
    doi = doi_acl

    cit = None
    attempts = 0
    while cit is None:
        cit = get_citations(doi)
        attempts += 1
        if attempts >= 2 and cit is None:
            print("Skipping", doi, "after 2 unsuccessful attempts")
            # try original DOI as fallback
            if doi != doi_orig:
                doi = doi_orig
                attempts = 0
            else:
                break

    data_new.append((doi_orig, cit))
    open(FILE_TGT, "w").write("\n".join([
        f"{doi}\t{cit}"
        for doi, cit in data_new
    ]))
