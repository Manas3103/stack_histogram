import ROOT

ROOT.gStyle.SetOptStat(0)

# ============================================================
# Input ROOT files
# ============================================================

files = {
    "eee": "eee_ThreeLRegion_Yield.root",
    "eeu": "eeu_ThreeLRegion_Yield.root",
    "uue": "uue_ThreeLRegion_Yield.root",
    "uuu": "uuu_ThreeLRegion_Yield.root"
}

regions = ["eee", "eeu", "uue", "uuu"]

# ============================================================
# MC processes
# ============================================================

mc_processes = [
    "DY",
    "tt+jets",
    "Xy",
    "VVV",
    "t(t)X",
    "ZZ",
    "WZ",
    "ttZ",
    "tZq"
]

# ============================================================
# Open files
# ============================================================

root_files = {}

for region, filename in files.items():

    root_files[region] = ROOT.TFile.Open(filename)

    if not root_files[region] or root_files[region].IsZombie():
        print(f"ERROR: Could not open {filename}")
        exit()


# ============================================================
# Canvas
# ============================================================

canvas = ROOT.TCanvas(
    "canvas",
    "Three Lepton Flavor Regions",
    900,
    800
)

canvas.Divide(1, 2)

# ============================================================
# Upper pad: Stacked MC + Data
# ============================================================

pad1 = canvas.cd(1)

pad1.SetPad(0.0, 0.30, 1.0, 1.0)
pad1.SetBottomMargin(0.02)
pad1.SetLeftMargin(0.12)
pad1.SetRightMargin(0.05)


# ============================================================
# Create MC stack
# ============================================================

stack = ROOT.THStack(
    "stack",
    ";Flavor Channel;Events"
)


# ============================================================
# Create histograms for MC
# ============================================================

mc_hists = {}


for process in mc_processes:

    hist = ROOT.TH1D(
        f"h_{process}",
        "",
        4,
        0,
        4
    )

    hist.SetDirectory(0)

    # X-axis labels
    hist.GetXaxis().SetBinLabel(1, "eee")
    hist.GetXaxis().SetBinLabel(2, "eeu")
    hist.GetXaxis().SetBinLabel(3, "uue")
    hist.GetXaxis().SetBinLabel(4, "uuu")

    # Fill each region
    for i, region in enumerate(regions, start=1):

        input_hist = root_files[region].Get(process)

        if not input_hist:
            print(
                f"WARNING: {process} not found in "
                f"{files[region]}"
            )
            continue

        yield_value = input_hist.Integral()

        error_squared = 0.0

        for bin_number in range(
            1,
            input_hist.GetNbinsX() + 1
        ):
            error_squared += (
                input_hist.GetBinError(bin_number) ** 2
            )

        yield_error = error_squared ** 0.5

        hist.SetBinContent(
            i,
            yield_value
        )

        hist.SetBinError(
            i,
            yield_error
        )

    mc_hists[process] = hist

    stack.Add(hist)


# ============================================================
# Draw stack
# ============================================================

pad1.cd()

stack.Draw("HIST")

stack.GetXaxis().SetLabelSize(0)
stack.GetXaxis().SetTitleSize(0)

stack.GetYaxis().SetTitle("Events")
stack.GetYaxis().SetTitleSize(0.055)
stack.GetYaxis().SetLabelSize(0.045)

stack.SetMinimum(0)

# ============================================================
# Data histogram
# ============================================================

data_hist = ROOT.TH1D(
    "data_hist",
    "",
    4,
    0,
    4
)

data_hist.SetDirectory(0)

for i, region in enumerate(regions, start=1):

    input_hist = root_files[region].Get("data")

    if not input_hist:
        print(
            f"WARNING: data not found in "
            f"{files[region]}"
        )
        continue

    data_value = input_hist.Integral()

    error_squared = 0.0

    for bin_number in range(
        1,
        input_hist.GetNbinsX() + 1
    ):
        error_squared += (
            input_hist.GetBinError(bin_number) ** 2
        )

    data_error = error_squared ** 0.5

    data_hist.SetBinContent(
        i,
        data_value
    )

    data_hist.SetBinError(
        i,
        data_error
    )


data_hist.SetMarkerStyle(20)
data_hist.SetMarkerSize(1.2)
data_hist.SetLineWidth(2)

data_hist.Draw("E1 SAME")


# ============================================================
# Legend
# ============================================================

legend = ROOT.TLegend(
    0.68,
    0.50,
    0.94,
    0.88
)

legend.SetBorderSize(0)
legend.SetFillStyle(0)

for process in reversed(mc_processes):

    legend.AddEntry(
        mc_hists[process],
        process,
        "f"
    )

legend.AddEntry(
    data_hist,
    "Data",
    "lep"
)

legend.Draw()


# ============================================================
# Lower pad: Data / MC
# ============================================================

pad2 = canvas.cd(2)

pad2.SetPad(
    0.0,
    0.0,
    1.0,
    0.30
)

pad2.SetTopMargin(0.03)
pad2.SetBottomMargin(0.35)
pad2.SetLeftMargin(0.12)
pad2.SetRightMargin(0.05)


# ============================================================
# Calculate total MC per region
# ============================================================

ratio = ROOT.TH1D(
    "ratio",
    "",
    4,
    0,
    4
)

ratio.SetDirectory(0)

for i in range(1, 5):

    total_mc = 0.0
    total_mc_error_squared = 0.0

    for process in mc_processes:

        mc_value = mc_hists[process].GetBinContent(i)
        mc_error = mc_hists[process].GetBinError(i)

        total_mc += mc_value
        total_mc_error_squared += mc_error ** 2

    total_mc_error = total_mc_error_squared ** 0.5

    data_value = data_hist.GetBinContent(i)
    data_error = data_hist.GetBinError(i)

    if total_mc > 0:

        ratio_value = data_value / total_mc

        ratio_error = data_error / total_mc

        ratio.SetBinContent(
            i,
            ratio_value
        )

        ratio.SetBinError(
            i,
            ratio_error
        )


# ============================================================
# Draw ratio
# ============================================================

ratio.SetMarkerStyle(20)
ratio.SetMarkerSize(1.0)
ratio.SetLineWidth(2)

ratio.SetTitle("")

ratio.GetXaxis().SetTitle("Flavor Channel")
ratio.GetXaxis().SetTitleSize(0.12)
ratio.GetXaxis().SetTitleOffset(1.0)

ratio.GetXaxis().SetLabelSize(0.11)

ratio.GetYaxis().SetTitle("Data / MC")
ratio.GetYaxis().SetTitleSize(0.10)
ratio.GetYaxis().SetTitleOffset(0.45)

ratio.GetYaxis().SetLabelSize(0.09)

ratio.SetMinimum(0.5)
ratio.SetMaximum(1.5)

ratio.Draw("E1")


# ============================================================
# Draw Data/MC = 1 line
# ============================================================

line = ROOT.TLine(
    0,
    1,
    4,
    1
)

line.SetLineStyle(2)
line.SetLineWidth(2)

line.Draw("SAME")


# ============================================================
# Save plot
# ============================================================

canvas.cd()

canvas.SaveAs(
    "ThreeLRegion_flavor_yields.pdf"
)

canvas.SaveAs(
    "ThreeLRegion_flavor_yields.png"
)


# ============================================================
# Keep canvas open
# ============================================================

input(
    "Press Enter to exit..."
)
