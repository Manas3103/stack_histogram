#include "TFile.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "THStack.h"
#include "TLegend.h"
#include "TPad.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TLine.h"
#include "TKey.h"
#include <iostream>
#include <vector>
#include <map>

void PLOT_function(const char* inputFile) {
//  const char* inputFile = "TR_leadingLepton_pt.root";
//  const char* outputImage = "TR_leadingLepton_pt.png";
//  const char* axis_title = "TR_leadingLepton_pt";

  // Generate the output file name by removing the .root extension
  TString inputFileStr(inputFile);
  inputFileStr.ReplaceAll(".root", "");

  // Construct output image and axis title based on the input file name
  const char* outputImage = Form("%s.png", inputFileStr.Data());
  const char* axis_title = inputFileStr.Data();

  // Your plotting code
  std::cout << "Input file: " << inputFile << std::endl;
  std::cout << "Output image: " << outputImage << std::endl;
  std::cout << "Axis title: " << axis_title << std::endl;

  gStyle->SetOptStat(0);
  gStyle->SetPadTickX(1);
  gStyle->SetPadTickY(1);
  gStyle->SetLegendBorderSize(0);
  gStyle->SetErrorX(0);

  TFile* file = TFile::Open(inputFile, "READ");
  if (!file || file->IsZombie()) {
    std::cerr << "Error opening file!" << std::endl;
    return;
  }

  std::vector<TH1D*> mcHists;
  TH1D* dataHist = nullptr;

  std::map<std::string, Color_t> colorMap = {
    {"tZq", kRed-7},
    {"ttZ", kGreen-7},
    {"WZ", kAzure-9},
    {"ZZ", kOrange-2},
    {"t(t)X", kViolet-7},
    {"VVV", kPink-3},
    {"Xy", kYellow-7},
    {"tt+jets", kGreen+1},
    {"DY", kBlue-6}
  };

  std::map<std::string, std::string> labelMap = {
    {"tZq", "tZq"},
    {"ttZ", "ttZ"},
    {"WZ", "WZ"},
    {"ZZ", "ZZ"},
    {"t(t)X", "t(t)X"},
    {"VVV", "VVV"},
    {"Xy", "X+Y"},
    {"tt+jets", "tt+jets"},
    {"DY", "DY"}
  };


  TIter next(file->GetListOfKeys());
  TKey* key;
  while ((key = (TKey*)next())) {
    TObject* obj = key->ReadObj();
    if (!obj->InheritsFrom("TH1D")) continue;

    TH1D* hist = (TH1D*)obj;
    std::string name = hist->GetName();

    if (name == "data") {
      dataHist = (TH1D*)hist->Clone("dataHist");
      dataHist->SetMarkerStyle(20);
      dataHist->SetMarkerSize(1.2);
      dataHist->SetMarkerColor(kBlack);
      dataHist->SetLineColor(kBlack);
      dataHist->SetLineWidth(2);
    } else {
      TH1D* clone = (TH1D*)hist->Clone((name + "_clone").c_str());
      std::string baseName = name; // default
      size_t pos = name.find("_");
      if (pos != std::string::npos) baseName = name.substr(0, pos);
      auto colorIt = colorMap.find(baseName);
      clone->SetFillColor(colorIt != colorMap.end() ? colorIt->second : kGray);
      clone->SetLineColor(kBlack);
      clone->SetLineWidth(1);
      mcHists.push_back(clone);
    }
  }

  if (!dataHist || mcHists.empty()) {
    std::cerr << "Missing data or MC histograms!" << std::endl;
    file->Close();
    return;
  }

  THStack* stack = new THStack("stack", "");
  TH1D* mcSum = (TH1D*)mcHists[0]->Clone("mcSum");
  mcSum->Reset();

  for (TH1D* hist : mcHists) {
    stack->Add(hist);
    mcSum->Add(hist);
  }

  TCanvas* canvas = new TCanvas("canvas", "Stack Plot", 800, 800);
  TPad* upperPad = new TPad("upperPad", "upperPad", 0, 0.3, 1, 1);
  TPad* lowerPad = new TPad("lowerPad", "lowerPad", 0, 0.05, 1, 0.3);
  upperPad->SetBottomMargin(0.02);
  upperPad->SetLeftMargin(0.12);
  upperPad->SetRightMargin(0.05);
  lowerPad->SetTopMargin(0.02);
  lowerPad->SetBottomMargin(0.3);
  lowerPad->SetLeftMargin(0.12);
  lowerPad->SetRightMargin(0.05);
  lowerPad->SetGridy();
  upperPad->Draw();
  lowerPad->Draw();

  upperPad->cd();
  double maxVal = std::max(stack->GetMaximum(), dataHist->GetMaximum()) * 1.8;
  stack->SetMaximum(maxVal);
  stack->SetMinimum(0.1);
  stack->Draw("HIST");
  dataHist->Draw("EP SAME");

  stack->GetYaxis()->SetTitle("Events");
  stack->GetYaxis()->SetTitleSize(0.05);
  stack->GetYaxis()->SetTitleOffset(1.2);
  stack->GetYaxis()->SetLabelSize(0.045);
  stack->GetXaxis()->SetLabelSize(0);

  // Improved legend position and labels
  TLegend* legend = new TLegend(0.65, 0.75, 0.95, 0.88);
  legend->SetNColumns(3);
  legend->AddEntry(dataHist, "Data", "EP");
  for (TH1D* hist : mcHists) {
    std::string fullName = hist->GetName(); // e.g., DY_clone
    std::string baseName = fullName.substr(0, fullName.find("_clone"));
    std::string label = (labelMap.find(baseName) != labelMap.end()) ? labelMap[baseName] : baseName;
    legend->AddEntry(hist, label.c_str(), "F");
  }
  legend->SetTextSize(0.04);
  // legend->SetNColumns(2); // Optional if you want two columns
  legend->Draw();

  TLatex latex;
  latex.SetNDC();
  latex.SetTextSize(0.03);
  latex.SetTextFont(61);
  latex.DrawLatex(0.18, 0.92, "CMS");

  TLatex prelim;
  prelim.SetNDC();
  prelim.SetTextSize(0.03);
  prelim.SetTextFont(52);
  prelim.DrawLatex(0.26, 0.92, "Work in progress");

  TLatex lumi;
  lumi.SetNDC();
  lumi.SetTextSize(0.04);
  lumi.SetTextFont(42);
  lumi.DrawLatex(0.65, 0.92, "8 fb^{-1} (13.6 TeV)");

  lowerPad->cd();
  TH1D* ratioHist = (TH1D*)dataHist->Clone("ratioHist");
  ratioHist->Divide(mcSum);
  ratioHist->SetTitle("");
  ratioHist->SetMarkerStyle(20);
  ratioHist->SetMarkerSize(1.2);
  ratioHist->GetXaxis()->SetTitle(axis_title);
  ratioHist->GetXaxis()->SetTitleSize(0.12);
  ratioHist->GetXaxis()->SetTitleOffset(1.0);
  ratioHist->GetXaxis()->SetLabelSize(0.10);
  ratioHist->GetYaxis()->SetTitle("Data/MC");
  ratioHist->GetYaxis()->SetTitleSize(0.12);
  ratioHist->GetYaxis()->SetTitleOffset(0.5);
  ratioHist->GetYaxis()->SetLabelSize(0.10);
  ratioHist->GetYaxis()->SetNdivisions(505);
  ratioHist->GetYaxis()->SetRangeUser(0,2);
  ratioHist->Draw("EP");

  TLine* line = new TLine(ratioHist->GetXaxis()->GetXmin(), 1, ratioHist->GetXaxis()->GetXmax(), 1);
  line->SetLineColor(kRed);
  line->SetLineStyle(2);
  line->Draw("SAME");

  canvas->SaveAs(outputImage);
  std::cout << "Plot saved as " << outputImage << std::endl;

  std::cout << "\nSummary:\n";
  std::cout << "Data = " << dataHist->Integral() << "\n";
  std::cout << "MC = " << mcSum->Integral() << "\n";
  std::cout << "Data/MC ratio = " << dataHist->Integral() / mcSum->Integral() << "\n";

  file->Close();
}

