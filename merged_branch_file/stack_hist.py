import ROOT
import os

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetErrorX(0)


class StackPlotter:
    def __init__(self, input_file):
        self.input_file = input_file
        self.base_name = os.path.splitext(input_file)[0]
        self.output_image = self.base_name + ".png"
        self.axis_title = self.base_name

        # Color map matching YOUR ROOT histogram names
        self.color_map = {
            "tZq": ROOT.kRed - 7,
            "ttZ": ROOT.kGreen - 7,
            "WZ": ROOT.kAzure - 9,
            "ZZ": ROOT.kOrange - 2,
            "t(t)X": ROOT.kViolet - 7,
            "VVV": ROOT.kPink - 3,
            "Xy": ROOT.kYellow - 7,
            "tt+jets": ROOT.kGreen + 1,
            "DY": ROOT.kBlue - 6,
        }

        # Labels for legend
        self.label_map = {
            "tZq": "tZq",
            "ttZ": "ttZ",
            "WZ": "WZ",
            "ZZ": "ZZ",
            "t(t)X": "t(t)X",
            "VVV": "VVV",
            "Xy": "X+Y",
            "tt+jets": "tt+jets",
            "DY": "DY",
        }

        self.mc_hists = []
        self.data_hist = None


    # ------------------------------------------
    # LOAD HISTOGRAMS SAFELY (FIXED)
    # ------------------------------------------
    def load_histograms(self):
        f = ROOT.TFile.Open(self.input_file)

        if not f or f.IsZombie():
            raise RuntimeError("Cannot open input ROOT file")

        print("\nHistograms found in file:")

        self.mc_hists = []
        self.data_hist = None

        for key in f.GetListOfKeys():
            name = key.GetName()
            class_name = key.GetClassName()
            print(f"  -> {name} ({class_name})")

            if not class_name.startswith("TH1"):
                continue

            hist = key.ReadObj()
            hist.SetDirectory(0)  # CRITICAL to prevent deletion

            # ---- DATA ----
            if name.lower() == "data":
                print("     [DATA detected]")
                self.data_hist = hist.Clone("dataHist")
                self.data_hist.SetDirectory(0)
                self.data_hist.SetMarkerStyle(20)
                self.data_hist.SetMarkerSize(1.2)
                self.data_hist.SetMarkerColor(ROOT.kBlack)
                self.data_hist.SetLineColor(ROOT.kBlack)
                self.data_hist.SetLineWidth(2)
                continue

            # ---- MC ----
            clone = hist.Clone(name + "_clone")
            clone.SetDirectory(0)

            base_name = name  # keep exact ROOT naming

            color = self.color_map.get(base_name, ROOT.kGray)

            clone.SetFillColor(color)
            clone.SetLineColor(ROOT.kBlack)
            clone.SetLineWidth(1)

            self.mc_hists.append(clone)

        f.Close()

        print("\nSummary after loading:")
        print("  Data hist:", "FOUND" if self.data_hist else "MISSING")
        print("  MC count:", len(self.mc_hists))

        if self.data_hist is None:
            raise RuntimeError("Missing Data histogram")

        if len(self.mc_hists) == 0:
            raise RuntimeError("Missing MC histograms")


    # ------------------------------------------
    # BUILD STACK
    # ------------------------------------------
    def build_stack(self):
        self.stack = ROOT.THStack("stack", "")

        # Sort MC by yield (CMS style)
        self.mc_hists.sort(key=lambda h: h.Integral())

        self.mc_sum = self.mc_hists[0].Clone("mcSum")
        self.mc_sum.Reset()

        for hist in self.mc_hists:
            self.stack.Add(hist)
            self.mc_sum.Add(hist)


    # ------------------------------------------
    # DRAW STACK + RATIO
    # ------------------------------------------
    def draw_plot(self):
        canvas = ROOT.TCanvas("canvas", "Stack Plot", 800, 800)

        upper = ROOT.TPad("upper", "upper", 0, 0.3, 1, 1)
        lower = ROOT.TPad("lower", "lower", 0, 0.05, 1, 0.3)

        upper.SetBottomMargin(0.02)
        upper.SetLeftMargin(0.12)
        upper.SetRightMargin(0.05)

        lower.SetTopMargin(0.02)
        lower.SetBottomMargin(0.3)
        lower.SetLeftMargin(0.12)
        lower.SetRightMargin(0.05)
        lower.SetGridy()

        upper.Draw()
        lower.Draw()

        # -------- UPPER PAD --------
        upper.cd()

        max_val = max(self.stack.GetMaximum(), self.data_hist.GetMaximum()) * 1.8

        self.stack.SetMaximum(max_val)
        self.stack.SetMinimum(0.1)
        self.stack.Draw("HIST")
        self.data_hist.Draw("EP SAME")

        self.stack.GetYaxis().SetTitle("Events")
        self.stack.GetYaxis().SetTitleSize(0.05)
        self.stack.GetYaxis().SetTitleOffset(1.2)
        self.stack.GetYaxis().SetLabelSize(0.045)
        self.stack.GetXaxis().SetLabelSize(0)

        # -------- LEGEND --------
        legend = ROOT.TLegend(0.65, 0.75, 0.95, 0.88)
        legend.SetNColumns(3)
        legend.AddEntry(self.data_hist, "Data", "EP")

        for hist in reversed(self.mc_hists):
            name = hist.GetName().replace("_clone", "")
            label = self.label_map.get(name, name)
            legend.AddEntry(hist, label, "F")

        legend.SetTextSize(0.04)
        legend.Draw()

        # -------- CMS TEXT --------
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextFont(61)
        latex.SetTextSize(0.03)
        latex.DrawLatex(0.18, 0.92, "CMS")

        prelim = ROOT.TLatex()
        prelim.SetNDC()
        prelim.SetTextFont(52)
        prelim.SetTextSize(0.03)
        prelim.DrawLatex(0.26, 0.92, "Work in progress")

        lumi = ROOT.TLatex()
        lumi.SetNDC()
        lumi.SetTextFont(42)
        lumi.SetTextSize(0.04)
        lumi.DrawLatex(0.65, 0.92, "8 fb^{-1} (13.6 TeV)")

        # -------- LOWER PAD (RATIO) --------
        lower.cd()

        ratio = self.data_hist.Clone("ratioHist")
        ratio.Divide(self.mc_sum)

        ratio.SetTitle("")
        ratio.SetMarkerStyle(20)
        ratio.SetMarkerSize(1.2)

        ratio.GetXaxis().SetTitle(self.axis_title)
        ratio.GetXaxis().SetTitleSize(0.12)
        ratio.GetXaxis().SetTitleOffset(1.0)
        ratio.GetXaxis().SetLabelSize(0.10)

        ratio.GetYaxis().SetTitle("Data/MC")
        ratio.GetYaxis().SetTitleSize(0.12)
        ratio.GetYaxis().SetTitleOffset(0.5)
        ratio.GetYaxis().SetLabelSize(0.10)
        ratio.GetYaxis().SetNdivisions(505)
        ratio.GetYaxis().SetRangeUser(0, 2)

        ratio.Draw("EP")

        line = ROOT.TLine(
            ratio.GetXaxis().GetXmin(), 1,
            ratio.GetXaxis().GetXmax(), 1
        )
        line.SetLineColor(ROOT.kRed)
        line.SetLineStyle(2)
        line.Draw("SAME")

        canvas.SaveAs(self.output_image)

        print("\nPlot saved as:", self.output_image)
        print("Data =", self.data_hist.Integral())
        print("MC =", self.mc_sum.Integral())
        print("Data/MC =", self.data_hist.Integral() / self.mc_sum.Integral())


# ------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------
def main():
    input_file = "TR_leadingLepton_pt.root"  # change if needed

    plotter = StackPlotter(input_file)
    plotter.load_histograms()
    plotter.build_stack()
    plotter.draw_plot()


if __name__ == "__main__":
    main()

