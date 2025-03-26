#!/usr/bin/env python3

import csv
import sys
import os
import os.path as p
from argparse import ArgumentParser

PathHint = str | bytes | os.PathLike

CUE = "cue"
RESP = "response"
NL = "NL"
EN = "EN"
NL_NAME = "nl_name"
EN_NAME = "en_name"
ACC = "accuracy"
NA = "NA"

SEP = ","


def fillin_corrects(trials: list[dict]) -> list[dict]:
    """Fills in 1 when correct, NA when . is in the response, leave
    empty otherwise"""
    for trial in trials:
        resp = trial[RESP]
        if resp == ".":
            trial[ACC] = NA
            continue

        acceptable = trial[NL_NAME] if trial[CUE] == NL else trial[EN_NAME]
        acceptable = [acceptable, "H_" + acceptable]

        if resp in acceptable:
            trial[ACC] = 1


def open_files(fn: PathHint, suffix: PathHint) -> None:
    """Opens the in- and output and corrects the files, the infile
    must exist and the output based on the suffix shouldn't.
    """

    base, ext = os.path.splitext(fn)
    outfn = base + suffix + ext

    if not p.exists(fn):
        raise RuntimeError(f"Oops the input {fn} doesn't exist")
    if p.exists(outfn):
        raise RuntimeError(
            f"Oops the output {outfn} already exist, I'm not overwriting it..."
        )

    rows = []

    with open(fn, "r") as input:
        reader = csv.DictReader(
            input,
        )
        rows = [row for row in reader]

    fillin_corrects(rows)

    with open(outfn, "w") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    """Run the program"""
    parser = ArgumentParser(
        "fill_in_corrects", "run this on a csv file, to fill in the corrects"
    )
    parser.add_argument("files", nargs="+", type=str, help="The input files")

    parser.add_argument(
        "-s", "--suffix", help="Determines the output name", default="_out"
    )

    args = parser.parse_args()

    for infile in args.files:
        open_files(infile, args.suffix)


if __name__ == "__main__":
    main()
