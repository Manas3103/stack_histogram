import ROOT
import os
from config import INPUT_DIR, OUTPUT_DIR, PROCESS_GROUPS, HISTOGRAM_BRANCHES


class HistogramMerger:
    def __init__(self):
        self.input_dir = INPUT_DIR
        self.output_dir = OUTPUT_DIR
        self.groups = PROCESS_GROUPS
        self.hist_branches = HISTOGRAM_BRANCHES

        os.makedirs(self.output_dir, exist_ok=True)

    def _get_reference_file(self):
        first_group = list(self.groups.values())[0]
        return os.path.join(self.input_dir, first_group[0])

    def discover_histograms(self):
        """Auto-detect histogram names if config list is empty"""

        if self.hist_branches:
            print("Using user-defined histogram list.")
            return self.hist_branches

        ref_path = self._get_reference_file()
        ref_file = ROOT.TFile.Open(ref_path)

        if not ref_file or ref_file.IsZombie():
            raise RuntimeError(f"Cannot open reference file: {ref_path}")

        hist_names = []
        for key in ref_file.GetListOfKeys():
            if key.GetClassName() == "TH1D":
                hist_names.append(key.GetName())

        ref_file.Close()
        print(f"Discovered {len(hist_names)} histograms automatically.")
        return hist_names

    def merge_single_histogram(self, hist_name):
        """Merge one histogram across process groups"""

        print(f"Processing: {hist_name}")

        out_path = os.path.join(self.output_dir, f"{hist_name}.root")
        out_file = ROOT.TFile(out_path, "RECREATE")

        for group_name, files in self.groups.items():
            merged_hist = None

            for fname in files:
                full_path = os.path.join(self.input_dir, fname)
                f = ROOT.TFile.Open(full_path)

                if not f or f.IsZombie():
                    print("Error opening:", full_path)
                    continue

                h = f.Get(hist_name)
                if not h:
                    print(f"Warning: {hist_name} missing in {full_path}")
                    f.Close()
                    continue

                if merged_hist is None:
                    merged_hist = h.Clone(group_name)
                    merged_hist.SetDirectory(0)
                else:
                    merged_hist.Add(h)

                f.Close()

            if merged_hist:
                out_file.cd()
                merged_hist.Write()
                merged_hist.Delete()

        out_file.Close()
        return out_path
"""
    def run(self):
        histograms = self.discover_histograms()

        for hist in histograms:
            self.merge_single_histogram(hist)

        print("Merge complete.")
"""
   def run(self):
        histograms = self.discover_histograms()
        merged_files = []

        for hist in histograms:
            out_path = self.merge_single_histogram(hist)
            if out_path:
                merged_files.append(out_path)

        print("Merge complete.")
        return merged_files

