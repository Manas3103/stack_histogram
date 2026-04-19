#include <TFile.h>
#include <TH1D.h>
#include <TKey.h>
#include <TClass.h>
#include <iostream>
#include <vector>
#include <string>
#include <map>

struct ProcessGroup {
    std::string name;
    std::vector<std::string> file_paths;
};

void merge_histograms() {
    std::vector<ProcessGroup> groups = {
        {"tZq", {"tzq_file_hist.root"}},
        {"ttZ", {"TTZToLLNuNu_M-10_hist.root", "TTZToLL_M-1to10_hist.root"}},
        {"WZ", {"WZTo3LNu_TuneCP5_hist.root"}},
        {"ZZ", {
            "ZTo4L_hist.root", "GluGluToContinToZZTo2l2l_hist.root",
            "GluGluToContinToZZTo4l_hist.root", "GluGluHToZZTo4L_M125_TuneCP5_hist.root",
            "VBF_HToZZTo4L_M125_TuneCP5_hist.root", "WminusH_HToZZTo4L_M125_TuneCP5_hist.root",
            "WplusH_HToZZTo4L_M125_TuneCP5_hist.root", "ZH_HToZZ_4LFilter_M125_TuneCP5_hist.root"
        }},
        {"t(t)X", {
            "TTWJetsToLNu_TuneCP5_hist.root", "ttHToNonbb_M125_TuneCP5_hist.root",
            "TTWH_hist.root", "TTWW_hist.root", "TTWZ_hist.root", "TTZH_hist.root",
            "TTZZ_hist.root", "TTHH_hist.root", "TTTT_hist.root", "THQ_hist.root",
            "THW_hist.root", "ST_tWll_hist.root"
        }},
        {"VVV", {"WWW_hist.root", "WWZ_hist.root", "WZZ_hist.root", "ZZZ_hist.root"}},
        {"Xy", {"TTGamma_Dilept_hist.root", "TGJets_TuneCP_hist.root",
                "ZGToLLG_hist.root", "WGToLNuG_hist.root"}},
        {"tt+jets", {"TTTo2L2Nu_hist.root", "TTToSemiLeptonic_hist.root"}},
        {"DY", {
            "DYJetsToLL_M-10to50_hist.root", "DYJetsToLL_M-50_HT_less_70_hist.root",
            "DYJetsToLL_M-50_HT-70to100_hist.root", "DYJetsToLL_M-50_HT-100to200_hist.root",
            "DYJetsToLL_M-50_HT-200to400_hist.root", "DYJetsToLL_M-50_HT-400to600_hist.root",
            "DYJetsToLL_M-50_HT-600to800_hist.root", "DYJetsToLL_M-50_HT-800to1200_hist.root",
            "DYJetsToLL_M-50_HT-1200to2500_hist.root", "DYJetsToLL_M-50_HT-2500toInf_hist.root"
        }},
	{"data", {"merged_data_hist_noNorm.root"}}
    };

    // First: Get list of histogram names from the first file
    std::vector<std::string> hist_names;
    TFile* refFile = TFile::Open(groups[0].file_paths[0].c_str());
    TIter next(refFile->GetListOfKeys());
    TKey* key;
    while ((key = (TKey*)next())) {
        if (key->GetClassName() == std::string("TH1D")) {
            hist_names.push_back(key->GetName());
        }
    }
    refFile->Close();

    // Output file
    TFile* outFile = new TFile("stack_input.root", "RECREATE");

    // Loop over histogram names
    for (const auto& hist_name : hist_names) {
        std::cout << "Processing: " << hist_name << std::endl;

        // Loop over process groups
        for (const auto& group : groups) {
            TH1D* mergedHist = nullptr;

            // Sum histograms for this group
            for (const auto& fname : group.file_paths) {
                TFile* f = TFile::Open(fname.c_str());
                if (!f || f->IsZombie()) {
                    std::cerr << "Error: Cannot open file " << fname << std::endl;
                    continue;
                }
                TH1D* h = (TH1D*)f->Get(hist_name.c_str());
                if (!h) {
                    std::cerr << "Warning: Histogram " << hist_name << " not found in " << fname << std::endl;
                    f->Close();
                    continue;
                }

                if (!mergedHist) {
                    mergedHist = (TH1D*)h->Clone((hist_name + "_" + group.name).c_str());
                    mergedHist->SetDirectory(0);
                } else {
                    mergedHist->Add(h);
                }
                f->Close();
            }

            // Save the combined histogram
            if (mergedHist) {
                outFile->cd();
                mergedHist->Write();
                delete mergedHist;
            }
        }
    }

    outFile->Close();
    std::cout << "Histograms merged and saved to stack_input.root" << std::endl;
}

