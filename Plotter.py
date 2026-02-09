import uproot
import awkward as ak
import hist
from hist import Hist
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import glob
import tqdm  # For progress bars

hep.style.use(hep.style.CMS)

class Process:
    """
    Represents a physics process. Automatically calculates sum_gen_weights
    from the 'Runs' tree across all files.
    """
    def __init__(self, name, file_pattern, xsec=None, is_data=False, tree_name='outputTree', runs_tree_name='Runs'):
        self.name = name
        self.files = glob.glob(file_pattern) if isinstance(file_pattern, str) else file_pattern
        self.xsec = xsec
        self.is_data = is_data
        self.tree_name = tree_name
        self.runs_tree_name = runs_tree_name
        
        # Determine Sum of Weights immediately upon initialization
        self.sum_gen_weights = self._calculate_total_sum_weights()

    def _calculate_total_sum_weights(self):
        """
        Scans all files in the process to sum the 'genEventSumw' branch 
        from the Runs tree.
        """
        if self.is_data:
            return 1.0 # Data doesn't need scaling

        print(f"[{self.name}] Calculating sum of gen weights from {len(self.files)} files...")
        total_sum = 0.0
        
        # We iterate over files to read just the Runs tree (fast)
        # Note: In NanoAOD, the branch is often 'genEventSumw'. 
        # Check your file if it is named differently (e.g. 'genEventSumw_' or 'sumGenWeight')
        for fname in tqdm.tqdm(self.files, desc="Scanning files"):
            try:
                with uproot.open(fname) as f:
                    # The Runs tree contains one entry per 'run' stored in the file.
                    # We must sum ALL entries in the Runs tree.
                    runs = f[self.runs_tree_name]
                    # 'genEventSumw' is the standard NanoAOD name. 
                    # If your code fails here, check the branch name in TBrowser.
                    if 'genEventSumw' in runs.keys():
                        total_sum += np.sum(runs['genEventSumw'].array())
                    elif 'genEventSumw_' in runs.keys(): # Sometimes happens in older versions
                        total_sum += np.sum(runs['genEventSumw_'].array())
                    else:
                        print(f"WARNING: 'genEventSumw' not found in {fname}. Setting partial sum to 0.")
            except Exception as e:
                print(f"Error reading {fname}: {e}")

        print(f"[{self.name}] Total Sum of Gen Weights: {total_sum:.2e}")
        return total_sum

    def load_data(self, variables, cut=None):
        """
        Loads variables + genWeight for the Events tree.
        """
        load_vars = variables + (['genWeight'] if not self.is_data else [])
        
        print(f"[{self.name}] Loading events...")
        events = uproot.concatenate(
            [f"{f}:{self.tree_name}" for f in self.files],
            expressions=load_vars,
            cut=cut,
            library="ak"
        )
        return events

class AnalysisManager:
    def __init__(self, luminosity):
        self.lumi = luminosity
        self.processes = []
        self.histograms = {}

    def add_process(self, process):
        self.processes.append(process)

    def process_and_fill(self, variable_name, bins, cut=None):
        axis = hist.axis.Variable(bins, name=variable_name, label=variable_name)
        
        for proc in self.processes:
            # 1. Load Data
            events = proc.load_data([variable_name], cut)
            
            if len(events) == 0:
                continue

            # 2. Calculate Final Weights
            if proc.is_data:
                # Data weight is always 1
                final_weights = np.ones(len(events))
            else:
                # MC Weight Formula:
                # (genWeight * xsec * Lumi) / sum_gen_weights_total
                
                gen_weights = events['genWeight']
                
                # Calculate the global scaling factor for this process
                scale_factor = (proc.xsec * self.lumi) / proc.sum_gen_weights
                
                # Broadcast scale factor to all events
                final_weights = gen_weights * scale_factor

            # 3. Fill Histogram
            h = Hist(axis, storage=hist.storage.Weight())
            h.fill(events[variable_name], weight=final_weights)
            self.histograms[proc.name] = h

    def get_histograms(self):
        return self.histograms

# --- Plotting Class (Same as before) ---
class CMSPlotter:
    def __init__(self, analysis_manager):
        self.manager = analysis_manager

    def plot_stack(self, output_name="plot.png", xlabel="Variable"):
        hists = self.manager.get_histograms()
        if not hists: return

        mc_hists = []
        mc_labels = []
        data_hist = None
        
        for name, h in hists.items():
            if "Data" in name or "data" in name:
                data_hist = h
            else:
                mc_hists.append(h)
                mc_labels.append(name)

        fig, (ax, rax) = plt.subplots(
            2, 1, figsize=(10, 10), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.05), sharex=True
        )

        if mc_hists:
            hep.histplot(mc_hists, ax=ax, stack=True, histtype="fill", label=mc_labels, sort='yield')
        if data_hist:
            hep.histplot(data_hist, ax=ax, histtype="errorbar", color="black", label="Data", yerr=True)

        ax.set_ylabel("Events")
        ax.set_yscale("log")
        ax.legend()
        hep.cms.label("Preliminary", data=True, lumi=f"{self.manager.lumi/1000:.1f}", com=13.6, loc=0, ax=ax)

        if data_hist and mc_hists:
            total_mc = sum(mc_hists)
            ratio = np.divide(data_hist.values(), total_mc.values(), out=np.zeros_like(data_hist.values()), where=total_mc.values()!=0)
            rax.plot(data_hist.axes[0].centers, ratio, 'ko', markersize=4)
            rax.axhline(1, color='gray', linestyle='--')
            rax.set_ylim(0.5, 1.5)
            rax.set_ylabel("Data / Pred.")
            rax.set_xlabel(xlabel)

        plt.savefig(output_name)
        print(f"Saved {output_name}")

# --- Execution ---
if __name__ == "__main__":
    # 1. Setup
    LUMI = 7000  # Example: 2018 Luminosity in pb^-1
    manager = AnalysisManager(LUMI)

    # 2. Add Processes
    # The code will now automatically open these files, go to the 'Runs' tree,
    # and sum the 'genEventSumw' branch to get the denominator.
    
    manager.add_process(Process("Signal", "processed_root_file/top_zq.root", xsec=6077.22))
    manager.add_process(Process("TTBar", "processed_root_file/ttbar_dilepton.root", xsec=831.76))
    manager.add_process(Process("Data", "processed_root_file/All_data_nodup.root", is_data=True))

    # 3. Run
    manager.process_and_fill("TR_leadingLepton_pt", np.linspace(0, 200, 21), cut="TR_leadingLepton_pt > 0")
    
    # 4. Plot
    plotter = CMSPlotter(manager)
    plotter.plot_stack("normalization_check.png", "Leading Lepton $p_T$ [GeV]")
