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
#include <vector>
#include <map>

void stack_variable_plot(const char* inputFile, const char* outputImage) {
  // List of MC processes in order for stacking
  std::vector<std::string> mc_order = {
    "DY", "tt+jets", "Xy", "VVV", "t(t)X", "ZZ", "WZ", "ttZ", "tZq"
  };

  // Color map for processes
  std::map<std::string, int> colorMap = {
    {"DY", kOrange-3}, {"tt+jets", kAzure+6}, {"Xy", kMagenta-7},
    {"VVV", kViolet-6}, {"t(t)X", kSpring-5}, {"ZZ", kCyan+2},
    {"WZ", kGreen+1}, {"ttZ", kBlue+1}, {"tZq", kRed}
  };

  gStyle->SetOptStat(0);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetErrorX(0);

  TFile* file = new TFile(inputFile, "READ");
  if (!file || file->IsZombie()) {
    std::cerr << "Error: Cannot open file " << inputFile << std::endl;
    return;
  }

  // Get the variable name (same for all histograms in file)
  TIter next(file->GetListOfKeys());
  TKey* key = (TKey*)next();
  if (!key) {
    std::cerr << "No keys found in the file." << std::endl;
    return;
  }
  std::string varName = key->ReadObj()->GetTitle();

  // Create MC stack and legend
  THStack* stack = new THStack("stack", "");
  TLegend* legend = new TLegend(0.65, 0.65, 0.90, 0.88);
  legend->SetTextSize(0.035);

  // Prepare MC sum histogram for ratio
  TH1D* mcSum = nullptr;

  // Add MC histograms to stack
  for (const auto& process : mc_order) {
    TH1D* h = (TH1D*)file->Get(process.c_str());
    if (!h) continue;

    h->SetFillColor(colorMap[process]);
    h->SetLineColor(colorMap[process]);
    h->SetLineWidth(1);

    stack->Add(h);

    if (!mcSum)
      mcSum = (TH1D*)h->Clone("mcSum");
    else
      mcSum->Add(h);

    legend->AddEntry(h, process.c_str(), "f");
  }

  // Get data histogram
  TH1D* dataHist = (TH1D*)file->Get("data");
  if (!dataHist) {
    std::cerr << "Data histogram not found!" << std::endl;
    return;
  }
  dataHist->SetMarkerStyle(20);
  dataHist->SetMarkerSize(1.2);
  dataHist->SetLineColor(kBlack);
  dataHist->SetLineWidth(2);
  legend->AddEntry(dataHist, "Data", "ep");

  // Create canvas and pads
  TCanvas* canvas = new TCanvas("canvas", "Stacked Plot", 800, 800);
  TPad* upperPad = new TPad("upperPad", "upperPad", 0, 0.3, 1, 1);
  upperPad->SetBottomMargin(0.02);
  upperPad->Draw();

  TPad* lowerPad = new TPad("lowerPad", "lowerPad", 0, 0.05, 1, 0.3);
  lowerPad->SetTopMargin(0.0);
  lowerPad->SetBottomMargin(0.25);
  lowerPad->SetGridy();
  lowerPad->Draw();

  // Draw upper pad
  upperPad->cd();
  stack->Draw("HIST");
  dataHist->Draw("EP SAME");

  stack->SetTitle("");
  stack->GetYaxis()->SetTitle("Events");
  stack->GetYaxis()->SetTitleSize(0.05);
  stack->GetYaxis()->SetLabelSize(0.045);
  stack->GetYaxis()->SetTitleOffset(1.2);
  stack->SetMaximum(dataHist->GetMaximum() * 1.5);
  stack->SetMinimum(0.1);

  // Axis setup (x-axis hidden on top pad)
  stack->GetXaxis()->SetLabelSize(0);

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
  lumiText.DrawLatex(0.60, 0.92, "41.48 fb^{-1} (13 TeV)");

  // Draw lower pad (ratio)
  lowerPad->cd();
  TH1D* ratioHist = (TH1D*)dataHist->Clone("ratio");
  ratioHist->Divide(mcSum);
  ratioHist->SetTitle("");
  ratioHist->GetXaxis()->SetTitle(varName.c_str());
  ratioHist->GetYaxis()->SetTitle("Data/MC");

  ratioHist->GetXaxis()->SetTitleSize(0.12);
  ratioHist->GetXaxis()->SetLabelSize(0.11);
  ratioHist->GetXaxis()->SetTitleOffset(1.0);

  ratioHist->GetYaxis()->SetTitleSize(0.12);
  ratioHist->GetYaxis()->SetLabelSize(0.11);
  ratioHist->GetYaxis()->SetTitleOffset(0.5);
  ratioHist->GetYaxis()->SetNdivisions(505);
  ratioHist->GetYaxis()->SetRangeUser(0.5, 1.5);

  ratioHist->Draw("EP");

  TLine* line = new TLine(ratioHist->GetXaxis()->GetXmin(), 1, ratioHist->GetXaxis()->GetXmax(), 1);
  line->SetLineColor(kRed+1);
  line->SetLineStyle(2);
  line->Draw("SAME");

  canvas->SaveAs(outputImage);
  std::cout << "✅ Saved plot as: " << outputImage << std::endl;

  std::cout << "\n==== Event Yields ====" << std::endl;
  std::cout << "Data: " << dataHist->Integral() << std::endl;
  std::cout << "Total MC: " << mcSum->Integral() << std::endl;
  std::cout << "Data/MC: " << dataHist->Integral() / mcSum->Integral() << std::endl;

  file->Close();
}

