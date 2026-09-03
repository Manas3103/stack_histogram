import ROOT

ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0)

# Open ROOT file
f = ROOT.TFile.Open("ThreeLRegion_nJets.root")

processes = [
    "WZ", "ZZ", "data"
]
# processes = [
#     "DY", "tt+jets", "WZ", "ZZ", "VVV",
#     "ttZ", "tZq", "t(t)X", "Xy", "data"
# ]
colors = {
    "WZ": ROOT.kGreen + 2,
    "ZZ": ROOT.kBlue + 1,
    "data": ROOT.kBlack,
}

canvas = ROOT.TCanvas("c", "Overlay MET Shapes", 900, 700)
canvas.SetLeftMargin(0.12)

legend = ROOT.TLegend(0.62, 0.52, 0.88, 0.88)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.03)

# THStack in NOSTACK mode overlays histograms
stack = ROOT.THStack("stack", "Three-Lepton Region: MET Shape Comparison")

histograms = []

for proc in processes:
    h = f.Get(proc)
    if not h:
        print(f"Missing histogram: {proc}")
        continue

    h = h.Clone(proc + "_shape")
    h.SetDirectory(0)

    # Normalize to unit area
    if h.Integral() > 0:
        h.Scale(1.0 / h.Integral())

    h.SetLineColor(colors[proc])
    h.SetLineWidth(2)
    h.SetFillStyle(0)

    if proc == "data":
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.8)

    histograms.append(h)
    stack.Add(h)
    legend.AddEntry(h, proc, "lep" if proc == "data" else "l")

# Draw all histograms overlaid
stack.Draw("NOSTACK HIST")

stack.GetXaxis().SetTitle("MET p_{T} [GeV]")
stack.GetYaxis().SetTitle("Normalized Events")
stack.SetMaximum(0.7)
stack.SetMinimum(0.0)
# Draw data points on top
for h in histograms:
    if h.GetName().startswith("data"):
        h.Draw("E SAME")

legend.Draw()

canvas.SaveAs("ThreeLRegion_nJet_overlay_shapes.png")
canvas.SaveAs("ThreeLRegion_nJet_overlay_shapes.pdf")

print("Saved overlay plots.")
