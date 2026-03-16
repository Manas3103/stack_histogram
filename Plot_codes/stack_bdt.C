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

void stack_bdt() {
  // Configuration
  const char* inputFile = "../bdt2_electron_histograms.root";
  const char* outputImage = "bdt2_electron_comparison.png";
 
  // Set ROOT style
  gStyle->SetOptStat(0);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetErrorX(0);
 
  // Open the ROOT file
  TFile* rootFile = new TFile(inputFile, "READ");
  if (!rootFile || rootFile->IsZombie()) {
    std::cerr << "Error: Input file " << inputFile << " not found or corrupted!" << std::endl;
    return;
  }
 
  // Load histograms
  TH1D* signalHist = (TH1D*)rootFile->Get("signal");
  TH1D* ttbarHist = (TH1D*)rootFile->Get("ttbar");
  TH1D* wjetsHist = (TH1D*)rootFile->Get("wjets");
  TH1D* dataHist = (TH1D*)rootFile->Get("data");
 
  if (!signalHist || !ttbarHist || !wjetsHist || !dataHist) {
    std::cerr << "Error: One or more histograms not found in the file!" << std::endl;
    rootFile->Close();
    delete rootFile;
    return;
  }
 
  // Set histogram styles
  signalHist->SetFillColor(kRed-7);
  signalHist->SetLineColor(kRed);
  signalHist->SetLineWidth(2);
 
  ttbarHist->SetFillColor(kGreen-7);
  ttbarHist->SetLineColor(kGreen+2);
  ttbarHist->SetLineWidth(1);
 
  wjetsHist->SetFillColor(kAzure-9);
  wjetsHist->SetLineColor(kBlue);
  wjetsHist->SetLineWidth(1);
 
  dataHist->SetMarkerStyle(20);
  dataHist->SetMarkerSize(1.2);
  dataHist->SetMarkerColor(kBlack);
  dataHist->SetLineColor(kBlack);
  dataHist->SetLineWidth(2);
 
  // Create MC stack
  THStack* mcStack = new THStack("mcStack", "");
  mcStack->Add(wjetsHist);
  mcStack->Add(ttbarHist);
  mcStack->Add(signalHist);
 
  // Create a sum histogram for the ratio calculation
  TH1D* mcSum = (TH1D*)signalHist->Clone("mcSum");
  mcSum->Add(ttbarHist);
  mcSum->Add(wjetsHist);
 
  // Create canvas with two pads
  TCanvas* canvas = new TCanvas("canvas", "BDT Analysis", 800, 800);
  canvas->cd();
 
  // Main pad for histograms
  TPad* upperPad = new TPad("upperPad", "upperPad", 0, 0.3, 1, 1);
  upperPad->SetBottomMargin(0.02);
  upperPad->SetLeftMargin(0.12);
  upperPad->SetRightMargin(0.05);
//  upperPad->SetLogy();  // Log scale for better visibility
  upperPad->Draw();
 
  // Ratio pad
  TPad* lowerPad = new TPad("lowerPad", "lowerPad", 0, 0.05, 1, 0.3);
  lowerPad->SetTopMargin(0);
  lowerPad->SetBottomMargin(0.25);
  lowerPad->SetLeftMargin(0.12);
  lowerPad->SetRightMargin(0.05);
  lowerPad->SetGridy();
  lowerPad->Draw();
 
  // Draw histograms on upper pad
  upperPad->cd();
 
  // Get maximum for proper scaling
  Double_t dataMax = dataHist->GetMaximum();
  mcStack->Draw("HIST"); // Draw once to get the maximum
  Double_t mcMax = mcStack->GetMaximum();
  Double_t maxVal = std::max(dataMax, mcMax) * 1.3;
 
  mcStack->SetMaximum(maxVal);
  mcStack->SetMinimum(0.1);  // For log scale
 
  // Draw stack and data
  mcStack->Draw("HIST");
  dataHist->Draw("EP SAME");
 
  // Set axis labels for the stack
  mcStack->GetXaxis()->SetLabelSize(0);
  mcStack->GetYaxis()->SetTitle("Events");
  mcStack->GetYaxis()->SetTitleSize(0.05);
  mcStack->GetYaxis()->SetTitleOffset(1.2);
  mcStack->GetYaxis()->SetLabelSize(0.045);
 
  // Create legend
  TLegend* legend = new TLegend(0.65, 0.68, 0.90, 0.88);
  legend->AddEntry(dataHist, "Data", "EP");
  legend->AddEntry(signalHist, "Single Top (t-chan)", "F");
  legend->AddEntry(ttbarHist, "TTbar + tW", "F");
  legend->AddEntry(wjetsHist, "W+Jets + Other", "F");
  legend->SetTextSize(0.04);
  legend->Draw();
 
  // Add CMS text
  TLatex cmsText;
  cmsText.SetNDC();
  cmsText.SetTextSize(0.05);
  cmsText.SetTextFont(61);
  cmsText.DrawLatex(0.15, 0.92, "CMS");
 
  // Add "Preliminary" text
  TLatex prelimText;
  prelimText.SetNDC();
  prelimText.SetTextSize(0.04);
  prelimText.SetTextFont(52);
  prelimText.DrawLatex(0.26, 0.92, "Preliminary");
 
  // Add luminosity text
  TLatex lumiText;
  lumiText.SetNDC();
  lumiText.SetTextSize(0.04);
  lumiText.SetTextFont(42);
  lumiText.DrawLatex(0.65, 0.92, "41.48 fb^{-1} (13 TeV)");
 
  // Draw ratio plot on lower pad
  lowerPad->cd();
 
  // Create ratio histogram
  TH1D* ratioHist = (TH1D*)dataHist->Clone("ratioHist");
  ratioHist->Divide(mcSum);
  ratioHist->SetTitle("");
 
  // Set ratio histogram style
  ratioHist->SetMarkerStyle(20);
  ratioHist->SetMarkerSize(1.2);
  ratioHist->GetXaxis()->SetTitle("BDT Score");
  ratioHist->GetXaxis()->SetTitleSize(0.12);
  ratioHist->GetXaxis()->SetTitleOffset(0.9);
  ratioHist->GetXaxis()->SetLabelSize(0.11);
 
  ratioHist->GetYaxis()->SetTitle("Data/MC");
  ratioHist->GetYaxis()->SetTitleSize(0.12);
  ratioHist->GetYaxis()->SetTitleOffset(0.5);
  ratioHist->GetYaxis()->SetLabelSize(0.11);
  ratioHist->GetYaxis()->SetNdivisions(505);
  ratioHist->GetYaxis()->SetRangeUser(0.5, 1.5);  // Set y-range for ratio plot
 
  ratioHist->Draw("EP");
 
  // Draw horizontal line at y=1
  TLine* line = new TLine(ratioHist->GetXaxis()->GetXmin(), 1, ratioHist->GetXaxis()->GetXmax(), 1);
  line->SetLineColor(kRed);
  line->SetLineStyle(2);
  line->Draw("SAME");
 
  // Save the output
  canvas->SaveAs(outputImage);
  std::cout << "Plot saved as " << outputImage << std::endl;
 
  // Print some statistics
  std::cout << "\nHistogram Statistics:" << std::endl;
  std::cout << "Signal events: " << signalHist->Integral() << std::endl;
  std::cout << "TTbar events: " << ttbarHist->Integral() << std::endl;
  std::cout << "W+Jets events: " << wjetsHist->Integral() << std::endl;
  std::cout << "Total MC events: " << mcSum->Integral() << std::endl;
  std::cout << "Data events: " << dataHist->Integral() << std::endl;
  std::cout << "Data/MC ratio: " << dataHist->Integral()/mcSum->Integral() << std::endl;
 
  // Clean up
  delete line;
  delete canvas;
  rootFile->Close();
  delete rootFile;
}

// Main function for standalone execution
//void plot_bdt_histograms() {
//  plotBDTHistograms();
///}
