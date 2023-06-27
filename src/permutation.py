#!/usr/bin/env python3

import numpy as np
import random
import argparse

args = argparse.ArgumentParser()
args.add_argument(
    "-fm", "--file-main", nargs="+",
    default=["data/2020.emnlp-main.cit2023.tsv"]
)
args.add_argument(
    "-ff", "--file-findings", nargs="+",
    default=["data/2020.emnlp-findings.cit2023.tsv"]
)
args = args.parse_args()


def read(fnames):
    lst = []
    for fname in fnames:
        with open(fname, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                split = line.strip().split("\t")
                lst.append(int(split[1]))
    return lst


data_main = read(args.file_main)
data_find = read(args.file_findings)


def permute(m, f):
    both = m + f
    random.shuffle(both)
    p1, p2 = both[:len(m)], both[len(m):]

    # basic santiy checks
    assert len(p1) + len(p2) == len(m) + len(f)
    assert sum(both) == sum(p1 + p2)

    return p1, p2


def test(m, f, statistic, comp, permutations=10000):
    count = 0.0
    sum1, sum2 = 0.0, 0.0
    for _ in range(permutations):
        p1, p2 = permute(m, f)
        if comp(statistic(p1), statistic(m)):
            count += 1
        sum1 += statistic(p1)
        sum2 += statistic(p2)

    return (count + 1) / (permutations + 1)


# comparison directions
def high(x, y): return x >= y
def low(x, y): return y <= x

# other test statistics


def gtr5(x): return len(list(filter(lambda e: e >= 5, x))) / float(len(x))
def gtr10(x): return len(list(filter(lambda e: e >= 10, x))) / float(len(x))
def gtr100(x): return len(list(filter(lambda e: e >= 100, x))) / float(len(x))
def gtr200(x): return len(list(filter(lambda e: e >= 200, x))) / float(len(x))


# run the unpaired permutation tests
for (desc, statistic, comp) in [
        ("mean", np.mean, high),
        ("median", np.median, high),
        ("std", np.std, low),
        (">= 5", gtr5, high),
        (">= 10", gtr10, high),
        (">= 100", gtr100, high),
        (">= 200", gtr200, high)
]:
    print(
        f"{desc.upper():<10}",
        f"main: {statistic(data_main):7.3f}",
        f"findings: {statistic(data_find):7.3f}",
        f"p-value {test(data_main, data_find, statistic, comp):.5f}"
    )
