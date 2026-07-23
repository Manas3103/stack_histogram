import ROOT
import glob
import json
import os

# Find all *_Yield.root files
root_files = sorted(glob.glob("*_Yield.root"))
print(root_files)
if not root_files:
    print("No *_Yield.root files found.")
    exit()

all_data = {}

for filename in root_files:
    print(f"Processing: {filename}")

    root_file = ROOT.TFile.Open(filename, "READ")

    if not root_file or root_file.IsZombie():
        print(f"ERROR: Could not open {filename}")
        continue

    file_data = {}

    # Loop over all objects in the ROOT file
    for key in root_file.GetListOfKeys():

        obj = key.ReadObj()

        # Only process TH1 histograms
        if not obj.InheritsFrom("TH1"):
            continue

        hist_name = obj.GetName()

        hist_data = {
            "integral": float(obj.Integral()),
            "nbins": int(obj.GetNbinsX()),
            "bins": []
        }

        # Store every bin
        for i in range(1, obj.GetNbinsX() + 1):

            bin_data = {
                "bin": i,
                "low_edge": float(obj.GetBinLowEdge(i)),
                "up_edge": float(obj.GetBinLowEdge(i) + obj.GetBinWidth(i)),
                "value": float(obj.GetBinContent(i)),
                "error": float(obj.GetBinError(i))
            }

            hist_data["bins"].append(bin_data)

        file_data[hist_name] = hist_data

    all_data[filename] = file_data

    root_file.Close()


# ============================================================
# Write JSON
# ============================================================

with open("yield_values.json", "w") as f:
    json.dump(all_data, f, indent=4)

print("\nWritten: yield_values.json")


# ============================================================
# Write TXT
# ============================================================

with open("yield_values.txt", "w") as f:

    for filename, histograms in all_data.items():

        f.write("=" * 80 + "\n")
        f.write(f"FILE: {filename}\n")
        f.write("=" * 80 + "\n\n")

        for hist_name, hist_data in histograms.items():

            f.write("-" * 60 + "\n")
            f.write(f"HISTOGRAM: {hist_name}\n")
            f.write(f"TOTAL INTEGRAL: {hist_data['integral']}\n")
            f.write(f"NUMBER OF BINS: {hist_data['nbins']}\n")
            f.write("-" * 60 + "\n")

            for b in hist_data["bins"]:

                f.write(
                    f"Bin {b['bin']:4d} | "
                    f"Range [{b['low_edge']:.6g}, {b['up_edge']:.6g}] | "
                    f"Value = {b['value']:.10g} | "
                    f"Error = {b['error']:.10g}\n"
                )

            f.write("\n")

print("Written: yield_values.txt")
print("\nDone.")
