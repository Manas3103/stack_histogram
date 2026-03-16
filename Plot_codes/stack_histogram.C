#include <TFile.h>
#include <TH1F.h>
#include <THStack.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TRatioPlot.h>
#include <TStyle.h>
#include <iostream>
#include <map>
#include <vector>
#include <string>

// Define histogram name to plot (can be changed to any histogram in your files)
std::string histogram_name =  "nElectron";// Change this variable to plot different histograms

// Define process groups with colors
struct ProcessGroup {
    std::string name;
    int color;
    std::vector<std::string> files;
};

// Define all process groups with their colors and files
std::vector<ProcessGroup> process_groups = {
    {
        "tZq",
        kBlue,
        {
            "tzq_file_hist.root"
        }
    },
    {
        "ttZ",
        kGreen,
        {
            "TTZToLLNuNu_M-10_hist.root",
            "TTZToLL_M-1to10_hist.root"
        }
    },
    {
        "WZ",
        kOrange+1,
        {
            "WZTo3LNu_TuneCP5_hist.root"
        }
    },
    {
        "ZZ",
        kYellow,
        {
            "ZTo4L_hist.root",
            "GluGluToContinToZZTo2l2l_hist.root",
            "GluGluToContinToZZTo4l_hist.root",
            "GluGluHToZZTo4L_M125_TuneCP5_hist.root",
            "VBF_HToZZTo4L_M125_TuneCP5_hist.root",
            "WminusH_HToZZTo4L_M125_TuneCP5_hist.root",
            "WplusH_HToZZTo4L_M125_TuneCP5_hist.root",
            "ZH_HToZZ_4LFilter_M125_TuneCP5_hist.root"
        }
    },
    {
        "t(t)X",
        kRed,
        {
            "TTWJetsToLNu_TuneCP5_hist.root",
            "ttHToNonbb_M125_TuneCP5_hist.root",
            "TTWH_hist.root",
            "TTWW_hist.root",
            "TTWZ_hist.root",
            "TTZH_hist.root",
            "TTZZ_hist.root",
            "TTHH_hist.root",
            "TTTT_hist.root",
            "THQ_hist.root",
            "THW_hist.root",
            "ST_tWll_hist.root"
        }
    },
    {
        "VVV",
        kMagenta,
        {
            "WWW_hist.root",
            "WWZ_hist.root",
            "WZZ_hist.root",
            "ZZZ_hist.root"
        }
    },
    {
        "Xy",
        kCyan,
        {
            "TTGamma_Dilept_hist.root",
            "TGJets_TuneCP_hist.root",
            "ZGToLLG_hist.root",
            "WGToLNuG_hist.root"
        }
    },
    {
        "tt +jets",
        kPink+1,
        {
            "TTTo2L2Nu_hist.root",
            "TTToSemiLeptonic_hist.root"
        }
    },
    {
        "DY",
        kTeal,
        {
            "DYJetsToLL_M-10to50_hist.root",
	    "DYJetsToLL_M-50_HT_less_70_hist.root",
            "DYJetsToLL_M-50_HT-70to100_hist.root",
            "DYJetsToLL_M-50_HT-100to200_hist.root",
            "DYJetsToLL_M-50_HT-200to400_hist.root",
            "DYJetsToLL_M-50_HT-400to600_hist.root",
            "DYJetsToLL_M-50_HT-600to800_hist.root",
            "DYJetsToLL_M-50_HT-800to1200_hist.root",
            "DYJetsToLL_M-50_HT-1200to2500_hist.root",
            "DYJetsToLL_M-50_HT-2500toInf_hist.root"
        }
    }
};

// Path to your data file
std::string data_file_path = "merged_data_hist_noNorm.root";

// Function to extract process name from filename
std::string extractProcessName(const std::string& filename) {
    // Extract just the file name without path
    size_t lastSlash = filename.find_last_of("/\\");
    std::string file = filename.substr(lastSlash + 1);
    
    // Extract the part after PROCESSED_ and before _hist.root
    size_t startPos = file.find("PROCESSED_") + 10;
    size_t endPos = file.find("_hist.root");
    
    return file.substr(startPos, endPos - startPos);
}

void stack_histogram() {
    gStyle->SetOptStat(0);
    
    // Create stack and legend
    THStack* stack = new THStack("stack", (histogram_name + " Distribution").c_str());
    TLegend* legend = new TLegend(0.6, 0.6, 0.9, 0.9);
    legend->SetBorderSize(0);
    legend->SetFillStyle(0);
    
    // Map to store the grouped histograms
    std::map<std::string, TH1F*> group_histograms;
    
    // Process each group
    for (const auto& group : process_groups) {
        TH1F* group_hist = nullptr;
        bool added_files = false;
        
        // Process each file in the group
        for (const auto& file_path : group.files) {
            TFile* file = TFile::Open(file_path.c_str(), "READ");
            if (!file || file->IsZombie()) {
                std::cerr << "Error: Failed to open " << file_path << std::endl;
                continue;
            }
            
            TH1F* hist = (TH1F*)file->Get(histogram_name.c_str());
            if (!hist) {
                std::cerr << "Error: Histogram '" << histogram_name << "' not found in " << file_path << std::endl;
                file->Close();
                continue;
            }
            
            // Clone the histogram to keep it after file close
            TH1F* hist_clone = (TH1F*)hist->Clone(extractProcessName(file_path).c_str());
            hist_clone->SetDirectory(0);
            
            // Add to group histogram or create it
            if (group_hist == nullptr) {
                group_hist = (TH1F*)hist_clone->Clone((group.name + "_hist").c_str());
                group_hist->SetDirectory(0);
                added_files = true;
            } else {
                group_hist->Add(hist_clone);
                added_files = true;
            }
            
            delete hist_clone;
            file->Close();
        }
        
        // Add the group histogram to the stack only if we actually added files
        if (group_hist && added_files) {
            group_hist->SetFillColor(group.color);
            group_hist->SetLineColor(group.color);
            stack->Add(group_hist);
            legend->AddEntry(group_hist, group.name.c_str(), "f");
            
            // Store in map to prevent garbage collection
            group_histograms[group.name] = group_hist;
        }
    }
    
    // Load data histogram
    TFile* data_file = TFile::Open(data_file_path.c_str(), "READ");
    if (!data_file || data_file->IsZombie()) {
        std::cerr << "Error: Failed to open data file!" << std::endl;
        return;
    }
    
    TH1F* data_hist = (TH1F*)data_file->Get(histogram_name.c_str());
    if (!data_hist) {
        std::cerr << "Error: Data histogram '" << histogram_name << "' not found!" << std::endl;
        data_file->Close();
        return;
    }
    
    // Clone the data histogram to keep it after file close
    TH1F* data_hist_clone = (TH1F*)data_hist->Clone("data_hist");
    data_hist_clone->SetDirectory(0);
    data_hist_clone->SetMarkerStyle(20);
    data_hist_clone->SetMarkerColor(kBlack);
    data_hist_clone->SetLineColor(kBlack);
    
    data_file->Close();
    
    // Create canvas with proper divisions for ratio plot
    TCanvas* canvas = new TCanvas("canvas", "Stacked Histogram with Ratio Plot", 800, 800);
    
    // Get total MC histogram (stack sum)
    stack->Draw("HIST");
    TH1F* mc_total = (TH1F*)stack->GetStack()->Last()->Clone("mc_total");
    mc_total->SetDirectory(0);
    
    // Create and draw ratio plot
    TRatioPlot* ratio_plot = new TRatioPlot(data_hist_clone, mc_total, "pois");
    ratio_plot->Draw();
    
    // Configure the upper pad (main plot)
    ratio_plot->GetUpperPad()->cd();
    stack->Draw("HIST");
    data_hist_clone->Draw("SAME E1");
    legend->AddEntry(data_hist_clone, "Data", "lep");
    legend->Draw();
    
    // Set axis titles for the main plot
    ratio_plot->GetUpperRefYaxis()->SetTitle("Events");
    ratio_plot->GetUpperRefXaxis()->SetTitle(histogram_name.c_str());
    
    // Configure the lower pad (ratio plot)
    ratio_plot->GetLowerPad()->cd();
    ratio_plot->GetLowerRefGraph()->GetYaxis()->SetTitle("Data/MC");
    ratio_plot->GetLowerRefGraph()->SetMinimum(0.5);
    ratio_plot->GetLowerRefGraph()->SetMaximum(1.5);
    
    // Set overall plot title
    canvas->cd();
    TPaveText* title = new TPaveText(0.1, 0.95, 0.9, 0.99, "brNDC");
    title->SetFillColor(0);
    title->SetBorderSize(0);
    title->SetTextAlign(21);
    title->AddText((histogram_name + " Distribution").c_str());
    title->Draw();
    
    // Save plot
    canvas->SaveAs(("stacked_" + histogram_name + "_with_ratio.png").c_str());
    
    std::cout << "Generated plot for histogram: " << histogram_name << std::endl;
    std::cout << "To plot a different histogram, change the 'histogram_name' variable." << std::endl;
}
