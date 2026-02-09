import ROOT
import os
from config import PROCESS_GROUPS, COLOR_MAP, MC_STACK_ORDER, PLOT_OUTPUT_DIR


class StackPlotter:
    def __init__(self, root_file):
        self.root_file = root_file
        self.data_hist = None
        self.mc_hists = []

        os.makedirs(PLOT_OUTPUT_DIR, exist_ok=True)

    def load_histograms(self):
        f = ROOT.TFile.Open(self.root_file)

        if not f or f.IsZombie():
            raise RuntimeError(f"Cannot open {self.root_file}")

        for key in f.GetListOfKeys():
            obj = key.ReadObj()

            if not obj.ClassName().startswith("TH1"):
                continue

            name = obj.GetName()

            # Detect DATA
            if name == "data":
                self.data_hist = obj.Clone("data")
                self.data_hist.SetMarkerStyle(20)
                self.data_hist.SetMarkerSize(1.1)
                self.data_hist.SetLineColor(ROOT.kBlack)

            else:
                h = obj.Clone(name)
                h.SetDirectory(0)
                self.mc_hists.append(h)

        f.Close()

        if not self.data_hist or not self.mc_hists:
            raise RuntimeError("Missing Data or MC histograms")

    def style_mc(self):
        for hist in self.mc_hists:
            for proc, color in COLOR_MAP.items():
                if proc in hist.GetName():
                    hist.SetFillColor(color)
                    hist.SetLineColor(ROOT.kBlack)

    def order_mc(self):
        ordered = []
        for proc in MC_STACK_ORDER:
            for hist in self.mc_hists:
                if proc in hist.GetName():
                    ordered.append(hist)

        self.mc_hists = ordered

    def draw(self):
        canvas = ROOT.TCanvas("c", "", 900, 750)
        stack = ROOT.THStack("stack", "")

        legend = ROOT.TLegend(0.65, 0.65, 0.88, 0.88)

        for hist in self.mc_hists:
            stack.Add(hist)
            legend.AddEntry(hist, hist.GetName(), "f")

        stack.Draw("HIST")

        if self.data_hist:
            self.data_hist.Draw("E SAME")
            legend.AddEntry(self.data_hist, "Data", "lep")

        stack.GetYaxis().SetTitle("Events")
        stack.GetXaxis().SetTitle(self.data_hist.GetXaxis().GetTitle())

        legend.Draw()

        base = os.path.basename(self.root_file).replace(".root", "")
        out_png = os.path.join(PLOT_OUTPUT_DIR, base + ".png")

        canvas.SaveAs(out_png)
        print(f"Saved plot → {out_png}")

    def run(self):
        self.load_histograms()
        self.style_mc()
        self.order_mc()
        self.draw()

