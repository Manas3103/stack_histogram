import ROOT
import os
from config import COLOR_MAP, MC_STACK_ORDER, PLOT_OUTPUT_DIR


class StackPlotter:
    def __init__(self, root_file):
        self.root_file = root_file
        self.data_hist = None
        self.mc_hists = []

        # Keep ROOT objects alive (CRITICAL in PyROOT)
        self._root_objs = []

        os.makedirs(PLOT_OUTPUT_DIR, exist_ok=True)

    # ==========================================================
    # Load histograms safely
    # ==========================================================
    def load_histograms(self):
        f = ROOT.TFile.Open(self.root_file)

        if not f or f.IsZombie():
            raise RuntimeError(f"Cannot open {self.root_file}")

        print(f"\nReading histograms from: {self.root_file}")

        for key in f.GetListOfKeys():
            obj = key.ReadObj()

            if not obj.InheritsFrom("TH1"):
                continue

            hist = obj.Clone(obj.GetName() + "_clone")
            hist.SetDirectory(0)

            name = hist.GetName()
            lname = name.lower()

            print("  Found:", name)

            # Detect DATA
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

    # ==========================================================
    # Style MC
    # ==========================================================
    def style_mc(self):
        for hist in self.mc_hists:
            for proc, color in COLOR_MAP.items():
                if proc in hist.GetName():
                    hist.SetFillColor(color)
                    hist.SetLineColor(ROOT.kBlack)
                    hist.SetLineWidth(1)

    # ==========================================================
    # Order MC
    # ==========================================================
    def order_mc(self):
        ordered = []
        for proc in MC_STACK_ORDER:
            for hist in self.mc_hists:
                if proc in hist.GetName():
                    ordered.append(hist)

        if ordered:
            self.mc_hists = ordered

    # ==========================================================
    # Build MC sum safely
    # ==========================================================
    def build_stack_sum(self):
        mc_sum = self.mc_hists[0].Clone("mc_sum")
        mc_sum.Reset()
        mc_sum.SetDirectory(0)

        for h in self.mc_hists:
            mc_sum.Add(h)

        return mc_sum

    # ==========================================================
    # Safe ratio division
    # ==========================================================
    def safe_ratio(self, num, den):
        ratio = num.Clone("ratio")
        ratio.SetDirectory(0)

        for i in range(1, ratio.GetNbinsX() + 1):
            d = den.GetBinContent(i)
            n = num.GetBinContent(i)

            if d > 0:
                ratio.SetBinContent(i, n / d)
                ratio.SetBinError(i, num.GetBinError(i) / d)
            else:
                ratio.SetBinContent(i, 0)
                ratio.SetBinError(i, 0)

        return ratio

    # ==========================================================
    # Draw everything safely
    # ==========================================================
    def draw(self):
        ROOT.gStyle.SetOptStat(0)

        canvas = ROOT.TCanvas("c", "", 900, 850)
        self._root_objs.append(canvas)

        upper = ROOT.TPad("upper", "", 0, 0.30, 1, 1)
        lower = ROOT.TPad("lower", "", 0, 0.05, 1, 0.30)

        upper.SetBottomMargin(0.02)
        lower.SetTopMargin(0.02)
        lower.SetBottomMargin(0.30)

        upper.Draw()
        lower.Draw()

        self._root_objs.extend([upper, lower])

        # =========================
        # Upper Pad
        # =========================
        upper.cd()

        stack = ROOT.THStack("stack", "")
        self._root_objs.append(stack)

        for h in self.mc_hists:
            stack.Add(h)

        stack.Draw("HIST")
        stack.GetStack().Last()  # FORCE BUILD

        mc_sum = self.build_stack_sum()
        self._root_objs.append(mc_sum)

        max_val = max(mc_sum.GetMaximum(), self.data_hist.GetMaximum()) * 1.40
        stack.SetMaximum(max_val)
        stack.SetMinimum(0)

        stack.GetYaxis().SetTitle("Events")
        stack.GetYaxis().SetTitleSize(0.05)
        stack.GetYaxis().SetLabelSize(0.045)
        stack.GetXaxis().SetLabelSize(0)

        # Uncertainty band
        unc_band = mc_sum.Clone("unc_band")
        unc_band.SetDirectory(0)
        unc_band.SetFillColor(ROOT.kGray + 2)
        unc_band.SetFillStyle(3004)
        unc_band.SetMarkerSize(0)
        unc_band.Draw("E2 SAME")
        self._root_objs.append(unc_band)

        self.data_hist.Draw("EP SAME")

        # =========================
        # Legend
        # =========================
        legend = ROOT.TLegend(0.65, 0.65, 0.88, 0.85)
        legend.SetBorderSize(0)
        legend.SetTextSize(0.028)
        legend.SetNColumns(2)

        legend.AddEntry(self.data_hist, "Data", "lep")

        for h in reversed(self.mc_hists):
            legend.AddEntry(h, h.GetName(), "f")

        legend.AddEntry(unc_band, "MC stat unc.", "f")
        legend.Draw()
        self._root_objs.append(legend)
        # =======================
        # CMS + Lumi Text (VISIBLE FIXED VERSION)
        # =======================
        upper.cd()

        # CMS
        cms = ROOT.TLatex()
        cms.SetNDC()
        cms.SetTextFont(61)
        cms.SetTextSize(0.055)
        cms.DrawLatex(0.18, 0.92, "CMS")

        # Work in Progress
        prelim = ROOT.TLatex()
        prelim.SetNDC()
        prelim.SetTextFont(52)
        prelim.SetTextSize(0.040)
        prelim.DrawLatex(0.27, 0.92, "Work in Progress")

        # Luminosity (right aligned)
        lumi = ROOT.TLatex()
        lumi.SetNDC()
        lumi.SetTextFont(42)
        lumi.SetTextSize(0.040)
        lumi.SetTextAlign(31)  # right align
        lumi.DrawLatex(0.90, 0.92, "110 fb^{-1} (13.6 TeV)")

        # Keep alive (VERY IMPORTANT in PyROOT)
        self._root_objs.extend([cms, prelim, lumi])



        # =========================
        # Ratio Panel
        # =========================
        lower.cd()

        ratio = self.safe_ratio(self.data_hist, mc_sum)
        ratio.SetMarkerStyle(20)
        ratio.SetMarkerSize(1.1)
        ratio.SetLineColor(ROOT.kBlack)

        ratio.GetYaxis().SetTitle("Data / MC")
        ratio.GetYaxis().SetNdivisions(505)
        ratio.GetYaxis().SetTitleSize(0.12)
        ratio.GetYaxis().SetLabelSize(0.10)
        ratio.GetYaxis().SetTitleOffset(0.45)
        ratio.GetYaxis().SetRangeUser(0.5, 1.5)

        x_title = self.data_hist.GetXaxis().GetTitle()
        if x_title == "":
            x_title = os.path.basename(self.root_file).replace(".root", "")

        ratio.GetXaxis().SetTitle(x_title)
        ratio.GetXaxis().SetTitleSize(0.12)
        ratio.GetXaxis().SetLabelSize(0.10)

        ratio.Draw("EP")
        self._root_objs.append(ratio)

        # Ratio uncertainty band
        unc_ratio = self.safe_ratio(unc_band, mc_sum)
        unc_ratio.SetFillColor(ROOT.kGray + 2)
        unc_ratio.SetFillStyle(3004)
        unc_ratio.SetMarkerSize(0)
        unc_ratio.Draw("E2 SAME")
        self._root_objs.append(unc_ratio)

        # Unity line
        line = ROOT.TLine(
            ratio.GetXaxis().GetXmin(),
            1,
            ratio.GetXaxis().GetXmax(),
            1
        )
        line.SetLineStyle(2)
        line.Draw("SAME")
        self._root_objs.append(line)

        # =========================
        # Save
        # =========================
        base = os.path.basename(self.root_file).replace(".root", "")
        out_png = os.path.join(PLOT_OUTPUT_DIR, base + ".png")

        canvas.SaveAs(out_png)
        print("Saved →", out_png)

    # ==========================================================
    def run(self):
        ROOT.gROOT.SetBatch(True)  # safer if not interactive
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetOptStat(0)

        self.load_histograms()
        self.style_mc()
        self.order_mc()
        self.draw()
