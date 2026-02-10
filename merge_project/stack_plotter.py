import ROOT
import os
from config import COLOR_MAP, MC_STACK_ORDER, PLOT_OUTPUT_DIR


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

        print(f"\nReading histograms from: {self.root_file}")

        for key in f.GetListOfKeys():
            obj = key.ReadObj()

            if not isinstance(obj, ROOT.TH1):
                continue

            hist = obj.Clone()
            hist.SetDirectory(0)

            name = hist.GetName()
            lname = name.lower()

            print("  Found:", name)

            # Detect DATA robustly
            if lname == "data" or "data" in lname:
                self.data_hist = hist
                self.data_hist.SetMarkerStyle(20)
                self.data_hist.SetMarkerSize(1.2)
                self.data_hist.SetLineColor(ROOT.kBlack)
                self.data_hist.SetLineWidth(2)

            else:
                self.mc_hists.append(hist)

        f.Close()

        if self.data_hist is None:
            raise RuntimeError("Missing DATA histogram")

        if len(self.mc_hists) == 0:
            raise RuntimeError("Missing MC histograms")

    def style_mc(self):
        for hist in self.mc_hists:
            for proc, color in COLOR_MAP.items():
                if proc in hist.GetName():
                    hist.SetFillColor(color)
                    hist.SetLineColor(ROOT.kBlack)
                    hist.SetLineWidth(1)

    def order_mc(self):
        ordered = []
        for proc in MC_STACK_ORDER:
            for hist in self.mc_hists:
                if proc in hist.GetName():
                    ordered.append(hist)

        if ordered:
            self.mc_hists = ordered

    def build_stack_sum(self):
        mc_sum = self.mc_hists[0].Clone("mc_sum")
        mc_sum.Reset()

        for h in self.mc_hists:
            mc_sum.Add(h)

        return mc_sum

    def draw(self):
        ROOT.gStyle.SetOptStat(0)

        canvas = ROOT.TCanvas("c", "", 900, 850)

        upper = ROOT.TPad("upper", "", 0, 0.30, 1, 1)
        lower = ROOT.TPad("lower", "", 0, 0.05, 1, 0.30)

        upper.SetBottomMargin(0.02)
        lower.SetTopMargin(0.02)
        lower.SetBottomMargin(0.30)

        upper.Draw()
        lower.Draw()

        # =======================
        # Upper pad (stack)
        # =======================
        upper.cd()

        stack = ROOT.THStack("stack", "")
        for h in self.mc_hists:
            stack.Add(h)

        stack.Draw("HIST")

        mc_sum = self.build_stack_sum()

        # Set Y max = stack max × 1.40
        max_val = max(stack.GetMaximum(), self.data_hist.GetMaximum()) * 1.40
        stack.SetMaximum(max_val)
        stack.SetMinimum(0)

        stack.GetYaxis().SetTitle("Events")
        stack.GetYaxis().SetTitleSize(0.05)
        stack.GetYaxis().SetLabelSize(0.045)
        stack.GetXaxis().SetLabelSize(0)

        # MC stat uncertainty band
        unc_band = mc_sum.Clone("unc_band")
        unc_band.SetFillColor(ROOT.kGray + 2)
        unc_band.SetFillStyle(3004)
        unc_band.SetMarkerSize(0)
        unc_band.Draw("E2 SAME")

        # Draw Data
        self.data_hist.Draw("EP SAME")

        # =======================
        # Legend
        # =======================
        legend = ROOT.TLegend(0.65, 0.65, 0.88, 0.85)  # LOWER + WIDER
        legend.SetBorderSize(0)
        legend.SetTextSize(0.028)  # SMALLER TEXT
        legend.SetNColumns(2)      # TWO COLUMNS (TWO ROWS EFFECT)

        legend.AddEntry(self.data_hist, "Data", "lep")

        for h in reversed(self.mc_hists):
            legend.AddEntry(h, h.GetName(), "f")

        legend.AddEntry(unc_band, "MC stat unc.", "f")
        legend.Draw()

        # =======================
        # CMS Text
        # =======================
        cms = ROOT.TLatex()
        cms.SetNDC()
        cms.SetTextFont(61)
        cms.SetTextSize(0.04)
        cms.DrawLatex(0.14, 0.92, "CMS")

        prelim = ROOT.TLatex()
        prelim.SetNDC()
        prelim.SetTextFont(52)
        prelim.SetTextSize(0.035)
        prelim.DrawLatex(0.22, 0.92, "Work in Progress")

        lumi = ROOT.TLatex()
        lumi.SetNDC()
        lumi.SetTextFont(42)
        lumi.SetTextSize(0.035)
        lumi.DrawLatex(0.68, 0.92, "8 fb^{-1} (13.6 TeV)")

        # =======================
        # Ratio panel
        # =======================
        lower.cd()

        ratio = self.data_hist.Clone("ratio")
        ratio.Divide(mc_sum)

        ratio.SetMarkerStyle(20)
        ratio.SetMarkerSize(1.1)
        ratio.SetLineColor(ROOT.kBlack)

        ratio.GetYaxis().SetTitle("Data / MC")
        ratio.GetYaxis().SetNdivisions(505)
        ratio.GetYaxis().SetTitleSize(0.12)
        ratio.GetYaxis().SetLabelSize(0.10)
        ratio.GetYaxis().SetTitleOffset(0.45)
        ratio.GetYaxis().SetRangeUser(0.3, 1.75)

        x_title = self.data_hist.GetXaxis().GetTitle()
        if x_title == "":
            x_title = os.path.basename(self.root_file).replace(".root", "")

        ratio.GetXaxis().SetTitle(x_title)
        ratio.GetXaxis().SetTitleSize(0.12)
        ratio.GetXaxis().SetLabelSize(0.10)

        ratio.Draw("EP")

        # MC uncertainty ratio band
        unc_ratio = unc_band.Clone()
        unc_ratio.Divide(mc_sum)
        unc_ratio.Draw("E2 SAME")

        # Unity line
        line = ROOT.TLine(
            ratio.GetXaxis().GetXmin(),
            1,
            ratio.GetXaxis().GetXmax(),
            1
        )
        line.SetLineStyle(2)
        line.Draw("SAME")

        bottom_title = ROOT.TLatex()
        bottom_title.SetNDC()
        bottom_title.SetTextFont(42)
        bottom_title.SetTextSize(0.032)
        bottom_title.SetTextAlign(22)  # Center alignment
        #bottom_title.DrawLatex(0.50, 0.02, os.path.basename(self.root_file).replace(".root", "manas"))


        # =======================
        # Save Output
        # =======================
        base = os.path.basename(self.root_file).replace(".root", "")
        out_png = os.path.join(PLOT_OUTPUT_DIR, base + ".png")

        canvas.SaveAs(out_png)
        print("Saved →", out_png)

    def run(self):
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetOptStat(0)

        self.load_histograms()
        self.style_mc()
        self.order_mc()
        self.draw()

