#include "TFile.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "THStack.h"
#include "TLegend.h"
#include "TPad.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TLine.h"
#include <iostream>
#include <map>
#include <vector>

void stack_bdt() {
  const char* inputFile = "combinedLeptonPt.root";
  const char* outputImage = "combinedLeptonPt.png";

  gStyle->SetOptStat(0);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetErrorX(0);

  TFile* rootFile = new TFile(inputFile, "READ");
  if (!rootFile || rootFile->IsZombie()) {
    std::cerr << "Error: Input file not found!" << std::endl;
    return;
  }

  std::vector<std::string> processNames = {
    "tZq", "ttZ", "WZ", "ZZ", "t(t)X", "VVV", "Xy", "tt+jets", "DY"
  };

  std::map<std::string, Color_t> colorMap = {
    {"tZq", kRed-7},
    {"ttZ", kOrange-3},
    {"WZ", kSpring-6},
    {"ZZ", kAzure+6},
    {"t(t)X", kViolet-5},
    {"VVV", kTeal+3},
    {"Xy", kYellow+2},
    {"tt+jets", kGreen+2},
    {"DY", kBlue-7}
  };

  THStack* mcStack = new THStack("mcStack", "");
  std::vector<TH1D*> mcHists;
  TH1D* mcSum = nullptr;

  // Load MC histograms
  for (const auto& proc : processNames) {
    std::string histName =  proc;
    TH1D* hist = (TH1D*)rootFile->Get(histName.c_str());
    if (!hist) {
      std::cerr << "Warning: Histogram " << histName << " not found!" << std::endl;
      continue;
    }

    hist->SetFillColor(colorMap[proc]);
    hist->SetLineColor(kBlack);
    hist->SetLineWidth(1);
    mcStack->Add(hist);
    mcHists.push_back(hist);

    if (!mcSum)
      mcSum = (TH1D*)hist->Clone("mcSum");
    else
      mcSum->Add(hist);
  }

  // Load data
  TH1D* dataHist = (TH1D*)rootFile->Get("data");
  if (!dataHist) {
    std::cerr << "Error: Data histogram not found!" << std::endl;
    return;
  }
  dataHist->SetMarkerStyle(20);
  dataHist->SetMarkerSize(1.2);
  dataHist->SetMarkerColor(kBlack);
  dataHist->SetLineColor(kBlack);
  dataHist->SetLineWidth(2);

  // Canvas
  TCanvas* canvas = new TCanvas("canvas", "Electron pt stack", 800, 800);

  TPad* upperPad = new TPad("upperPad", "upperPad", 0, 0.3, 1, 1);
  upperPad->SetBottomMargin(0.02);
  upperPad->Draw();

  TPad* lowerPad = new TPad("lowerPad", "lowerPad", 0, 0.05, 1, 0.3);
  lowerPad->SetTopMargin(0);
  lowerPad->SetBottomMargin(0.25);
  lowerPad->SetGridy();
  lowerPad->Draw();

  // Draw upper pad
  upperPad->cd();
  double maxVal = std::max(mcStack->GetMaximum(), dataHist->GetMaximum()) * 1.3;
  mcStack->SetMaximum(maxVal);
  mcStack->Draw("HIST");
  dataHist->Draw("EP SAME");

  mcStack->GetXaxis()->SetLabelSize(0);
  mcStack->GetYaxis()->SetTitle("Events");
  mcStack->GetYaxis()->SetTitleSize(0.05);
  mcStack->GetYaxis()->SetTitleOffset(1.2);
  mcStack->GetYaxis()->SetLabelSize(0.045);

  TLegend* legend = new TLegend(0.65, 0.50, 0.90, 0.88);
  legend->AddEntry(dataHist, "Data", "EP");
  for (size_t i = 0; i < mcHists.size(); ++i)
    legend->AddEntry(mcHists[i], processNames[i].c_str(), "F");
  legend->SetTextSize(0.035);
  legend->Draw();

  TLatex cmsText;
  cmsText.SetNDC();
  cmsText.SetTextSize(0.05);
  cmsText.SetTextFont(61);
  cmsText.DrawLatex(0.15, 0.92, "CMS");

  TLatex prelimText;
  prelimText.SetNDC();
  prelimText.SetTextSize(0.04);
  prelimText.SetTextFont(52);
  prelimText.DrawLatex(0.26, 0.92, "Preliminary");

  TLatex lumiText;
  lumiText.SetNDC();
  lumiText.SetTextSize(0.04);
  lumiText.SetTextFont(42);
  lumiText.DrawLatex(0.65, 0.92, "41.48 fb^{-1} (13 TeV)");

  // Ratio plot
  lowerPad->cd();
  TH1D* ratioHist = (TH1D*)dataHist->Clone("ratioHist");
  ratioHist->Divide(mcSum);
  ratioHist->SetTitle("");

  ratioHist->SetMarkerStyle(20);
  ratioHist->SetMarkerSize(1.2);
  ratioHist->GetXaxis()->SetTitle("Electron p_{T} [GeV]");
  ratioHist->GetXaxis()->SetTitleSize(0.12);
  ratioHist->GetXaxis()->SetTitleOffset(0.9);
  ratioHist->GetXaxis()->SetLabelSize(0.11);

  ratioHist->GetYaxis()->SetTitle("Data/MC");
  ratioHist->GetYaxis()->SetTitleSize(0.12);
  ratioHist->GetYaxis()->SetTitleOffset(0.5);
  ratioHist->GetYaxis()->SetLabelSize(0.11);
  ratioHist->GetYaxis()->SetNdivisions(505);
  ratioHist->GetYaxis()->SetRangeUser(0.5, 1.5);
  ratioHist->Draw("EP");

  TLine* line = new TLine(ratioHist->GetXaxis()->GetXmin(), 1, ratioHist->GetXaxis()->GetXmax(), 1);
  line->SetLineColor(kRed);
  line->SetLineStyle(2);
  line->Draw("SAME");

  // Save
  canvas->SaveAs(outputImage);
  std::cout << "Plot saved as " << outputImage << std::endl;

  std::cout << "\nHistogram Statistics:\n";
  for (size_t i = 0; i < mcHists.size(); ++i)
    std::cout << processNames[i] << " events: " << mcHists[i]->Integral() << std::endl;

  std::cout << "Total MC events: " << mcSum->Integral() << std::endl;
  std::cout << "Data events: " << dataHist->Integral() << std::endl;
  std::cout << "Data/MC ratio: " << dataHist->Integral() / mcSum->Integral() << std::endl;

  delete line;
  delete canvas;
  rootFile->Close();
  delete rootFile;
}

