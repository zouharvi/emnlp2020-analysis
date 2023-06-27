#!/usr/bin/env python3

from semanticscholar import SemanticScholar
import csv
import tqdm
import os
import time
import argparse

sch = SemanticScholar()

args = argparse.ArgumentParser()
args.add_argument("-p", "--prefix", default="findings2020")
args = args.parse_args()

FILE_SRC = f"data/{args.prefix}.cit2021.tsv"
FILE_TGT = f"data/{args.prefix}.cit2023.tsv"

data = [x["DOI"] for x in csv.DictReader(open(FILE_SRC, "r"), delimiter="\t")]


def get_citations(doi):
    try:
        paper = sch.get_paper(doi)
        x = paper.citationCount
        return x
    except:
        return None


if os.path.exists(FILE_TGT):
    data_new = [tuple(x.strip("\n").split("\t")) for x in open(FILE_TGT, "r")]
    data = data[len(data_new):]
else:
    data_new = []

for doi in tqdm.tqdm(data):
    cit = get_citations(doi)
    data_new.append((doi, cit))
    open(FILE_TGT, "w").write("\n".join([
        f"{doi}\t{cit}"
        for doi, cit in data_new
    ]))
