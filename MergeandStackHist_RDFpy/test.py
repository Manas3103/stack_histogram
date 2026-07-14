#!/usr/bin/env python3

import ROOT
import os
import json
import argparse

ROOT.gROOT.SetBatch(True)

def extract_hist_info(root_file):
    result = {}

    f = ROOT.TFile.Open(root_file)

    if not f or f.IsZombie():
        print(f"[ERROR] Cannot open {root_file}")
        return None

    for key in f.GetListOfKeys():
        obj = key.ReadObj()

        if not obj.InheritsFrom("TH1"):
            continue

        result[obj.GetName()] = {
            "integral": float(obj.Integral()),
            "entries": float(obj.GetEntries()),
            "mean": float(obj.GetMean()),
            "rms": float(obj.GetRMS()),
            "nbins": int(obj.GetNbinsX())
        }

    f.Close()
    return result


def main(input_dir, output_json):

    all_data = {}

    root_files = sorted(
        f for f in os.listdir(input_dir)
        if f.endswith(".root")
    )

    print(f"Found {len(root_files)} ROOT files")

    for fname in root_files:

        full_path = os.path.join(input_dir, fname)

        print(f"Processing {fname}")

        info = extract_hist_info(full_path)

        if info is not None:
            all_data[fname] = info

    with open(output_json, "w") as fp:
        json.dump(all_data, fp, indent=4)

    print(f"\nSaved JSON -> {output_json}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument(
        "-o",
        "--output",
        default="histogram_integrals.json"
    )

    args = parser.parse_args()

    main(args.input_dir, args.output)
