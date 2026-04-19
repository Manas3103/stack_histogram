#include <TFile.h>
#include <TH1D.h>
#include <TKey.h>
#include <TClass.h>
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <filesystem>  // Requires C++17

struct ProcessGroup {
    std::string name;
    std::vector<std::string> file_paths;
};

void merge_histograms_per_branch() {
    // Define input and output paths relative to current_dir
    std::string input_dir = "all_root_file";
    std::string output_dir = "merged_branch_file";

/*    std::vector<ProcessGroup> groups = {
        {"tZq", {"tzq_file_hist_new.root"}},
        {"ttZ", {"TTZToLLNuNu_M-10_hist_new.root", "TTZToLL_M-1to10_hist_new.root"}},
        {"WZ", {"WZTo3LNu_TuneCP5_hist_new.root"}},
        {"ZZ", {
            "ZTo4L_hist_new.root", "GluGluToContinToZZTo2l2l_hist_new.root",
            "GluGluToContinToZZTo4l_hist_new.root", "GluGluHToZZTo4L_M125_TuneCP5_hist_new.root",
            "VBF_HToZZTo4L_M125_TuneCP5_hist_new.root", "WminusH_HToZZTo4L_M125_TuneCP5_hist_new.root",
            "WplusH_HToZZTo4L_M125_TuneCP5_hist_new.root", "ZH_HToZZ_4LFilter_M125_TuneCP5_hist_new.root"
        }},
        {"t(t)X", {
            "TTWJetsToLNu_TuneCP5_hist_new.root", "ttHToNonbb_M125_TuneCP5_hist_new.root",
            "TTWH_hist_new.root", "TTWW_hist_new.root", "TTWZ_hist_new.root", "TTZH_hist_new.root",
            "TTZZ_hist_new.root", "TTHH_hist_new.root", "TTTT_hist_new.root", "THQ_hist_new.root",
            "THW_hist_new.root", "ST_tWll_hist_new.root"
        }},
        {"VVV", {"WWW_hist_new.root", "WWZ_hist_new.root", "WZZ_hist_new.root", "ZZZ_hist_new.root"}},
        {"Xy", {"TTGamma_Dilept_hist_new.root", "TGJets_TuneCP_hist_new.root",
                "ZGToLLG_hist_new.root", "WGToLNuG_hist_new.root"}},
        {"tt+jets", {"TTTo2L2Nu_hist_new.root", "TTToSemiLeptonic_hist_new.root"}},
        {"DY", {
            "DYJetsToLL_M-10to50_hist_new.root", "DYJetsToLL_M-50_HT_less_70_hist_new.root",
            "DYJetsToLL_M-50_HT-70to100_hist_new.root", "DYJetsToLL_M-50_HT-100to200_hist_new.root",
            "DYJetsToLL_M-50_HT-200to400_hist_new.root", "DYJetsToLL_M-50_HT-400to600_hist_new.root",
            "DYJetsToLL_M-50_HT-600to800_hist_new.root", "DYJetsToLL_M-50_HT-800to1200_hist_new.root",
            "DYJetsToLL_M-50_HT-1200to2500_hist_new.root", "DYJetsToLL_M-50_HT-2500toInf_hist_new.root"
        }},
        {"data", {"All_noNorm_hist_new.root"}}
    };*/

/*    //this is for the normal variable
    //"DYJetsToLL_M-50_HT_less_70_1_hist_new.root"
    std::vector<ProcessGroup> groups = {
        {"DY", {
            "DYJetsToLL_M-10to50_hist_new.root",
            "DYJetsToLL_M-50_HT-70to100_hist_new.root", "DYJetsToLL_M-50_HT-100to200_hist_new.root",
            "DYJetsToLL_M-50_HT-200to400_hist_new.root", "DYJetsToLL_M-50_HT-400to600_hist_new.root",
            "DYJetsToLL_M-50_HT-600to800_hist_new.root", "DYJetsToLL_M-50_HT-800to1200_hist_new.root",
            "DYJetsToLL_M-50_HT-1200to2500_hist_new.root", "DYJetsToLL_M-50_HT-2500toInf_hist_new.root"
        }},
        {"tt+jets", {"TTTo2L2Nu_hist_new.root", "TTToSemiLeptonic_hist_new.root"}},
        {"Xy", {"TTGamma_Dilept_hist_new.root", "TGJets_TuneCP_hist_new.root",
                "ZGToLLG_hist_new.root", "WGToLNuG_hist_new.root"}},
        {"VVV", {"WWW_hist_new.root", "WWZ_hist_new.root", "WZZ_hist_new.root", "ZZZ_hist_new.root"}},
        {"t(t)X", {
            "TTWJetsToLNu_TuneCP5_hist_new.root", "ttHToNonbb_M125_TuneCP5_hist_new.root",
            "TTWH_hist_new.root", "TTWW_hist_new.root", "TTWZ_hist_new.root", "TTZH_hist_new.root",
            "TTZZ_hist_new.root", "TTHH_hist_new.root", "TTTT_hist_new.root", "THQ_hist_new.root",
            "THW_hist_new.root", "ST_tWll_hist_new.root"
        }},
        {"ZZ", {
            "ZTo4L_hist_new.root", "GluGluToContinToZZTo2l2l_hist_new.root",
            "GluGluToContinToZZTo4l_hist_new.root", "GluGluHToZZTo4L_M125_TuneCP5_hist_new.root",
            "VBF_HToZZTo4L_M125_TuneCP5_hist_new.root", "WminusH_HToZZTo4L_M125_TuneCP5_hist_new.root",
            "WplusH_HToZZTo4L_M125_TuneCP5_hist_new.root", "ZH_HToZZ_4LFilter_M125_TuneCP5_hist_new.root"
        }},
        {"WZ", {"WZTo3LNu_TuneCP5_hist_new.root"}},
        {"ttZ", {"TTZToLLNuNu_M-10_hist_new.root", "TTZToLL_M-1to10_hist_new.root"}},
        {"tZq", {"tzq_file_hist_new.root"}},
        {"data", {"All_merged_file_hist_noNorm.root"}}
    };

std::vector<ProcessGroup> groups = {
    {"DY", {
        "dy_10to50_hist_new.root",
        "dy_m50_hist_new.root"
    }},
    {"tt+jets", {
        "ttbar_dilepton_hist_new.root",
        "ttbar_semilep_hist_new.root"
    }},
    {"Xy", {
        "zg_ntgc_hist_new.root",
	"tgqb_hist_new.root",
        "wg_10to100_hist_new.root"
    }},
    {"VVV", {
        "www_hist_new.root",
        "wwz_hist_new.root",
        "wzz_hist_new.root",
        "zzz_hist_new.root"
    }},
    {"t(t)X", {
        "tth_non2b_hist_new.root",
        "ttwh_hist_new.root",
        "ttww_hist_new.root",
        "ttzh_hist_new.root",
        "ttzz_hist_new.root",
        "tttt_hist_new.root",
        "thq_hist_new.root",
	"tbarb_lmin_hist_new.root",
	"tbbar_lplus_hist_new.root",
        "thw_hist_new.root"
    }},
    {"ZZ", {
        "ggh_zz_4l_hist_new.root",
        "gg_zz_2mu2tau_hist_new.root",
        "gg_zz_2e2tau_hist_new.root",
        "gg_zz_2e2mu_hist_new.root",
	"gg_zz_4e_hist_new.root",
	"gg_zz_4mu_hist_new.root",
        "vbfh_zz_4l_hist_new.root",
        "wmh_zz_4l_hist_new.root",
	"wph_zz_4l_hist_new.root",
	"zz_hist_new.root"
    }},
    {"WZ", {
        "wz_hist_new.root"
    }},
    {"ttZ", {
        "ttz_4to50_hist_new.root",
        "ttz_50_hist_new.root"
    }},
    {"tZq", {
        "top_zq_hist_new.root"
    }},
    {"data", {
        "All_data_nodup_hist_noNorm.root"
    }}
};*/
std::vector<ProcessGroup> groups = {
    {"tt+jets", {
        "ttbar_dilepton_part1_skimed_hist_new.root",
        "ttbar_dilepton_part2_skimed_hist_new.root",
        "ttbar_dilepton_part3_skimed_hist_new.root",
        "ttbar_semilep_skimed_hist_new.root"
    }},
    {"VVV", {
        "www_hist_new.root",
        "wwz_hist_new.root",
        "wzz_hist_new.root",
        "zzz_hist_new.root"
    }},
    {"t(t)X", {
        "ttwh_hist_new.root",
        "ttww_hist_new.root",
        "ttwz_hist_new.root",   // added (exists in your files)
        "tbarb_lmin_hist_new.root",
        "tbbar_lplus_hist_new.root"
        // removed: tth_non2b, ttzh, ttzz, tttt, thq, thw (not present)
    }},
    {"ZZ", {
        "ggh_zz_4l_hist_new.root",
        "vbfh_zz_4l_hist_new.root",
        "wmh_zz_4l_hist_new.root",
        "wph_zz_4l_hist_new.root"
        // removed all gg_zz_* and zz_hist_new.root (not present)
    }},
    {"WZ", {
        "wz_3lnu_skimed_hist_new.root"
    }},
    {"ttZ", {
        "ttz_4to50_hist_new.root",
        "ttz_50_hist_new.root"
    }},
    {"tZq", {
        "top_zq_hist_new.root"
    }},
    {"data", {
        "All_data_nodup_hist_noNorm.root"
    }}
};
    // Ensure output directory exists
    std::filesystem::create_directories(output_dir);

    // Use the first file as a reference to get all histogram names
    std::string ref_file_path = input_dir + "/" + groups[0].file_paths[0];
    TFile* refFile = TFile::Open(ref_file_path.c_str());
    if (!refFile || refFile->IsZombie()) {
        std::cerr << "Error: Cannot open reference file " << ref_file_path << std::endl;
        return;
    }

    std::vector<std::string> hist_names;
    TIter next(refFile->GetListOfKeys());
    TKey* key;
    while ((key = (TKey*)next())) {
        if (key->GetClassName() == std::string("TH1D")) {
            hist_names.push_back(key->GetName());
        }
    }
    refFile->Close();

    // Loop over each histogram name
    for (const auto& hist_name : hist_names) {
        std::cout << "Processing: " << hist_name << std::endl;

        std::string out_file_path = output_dir + "/" + hist_name + ".root";
        TFile* outFile = new TFile(out_file_path.c_str(), "RECREATE");

        for (const auto& group : groups) {
            TH1D* mergedHist = nullptr;

            for (const auto& fname : group.file_paths) {
                std::string full_path = input_dir + "/" + fname;
                TFile* f = TFile::Open(full_path.c_str());
                if (!f || f->IsZombie()) {
                    std::cerr << "Error: Cannot open " << full_path << std::endl;
                    continue;
                }

                TH1D* h = (TH1D*)f->Get(hist_name.c_str());
                if (!h) {
                    std::cerr << "Warning: Histogram " << hist_name << " not found in " << full_path << std::endl;
                    f->Close();
                    continue;
                }

                if (!mergedHist) {
                    mergedHist = (TH1D*)h->Clone(group.name.c_str());
                    mergedHist->SetDirectory(0);
                } else {
                    mergedHist->Add(h);
                }
                f->Close();
            }

            if (mergedHist) {
                outFile->cd();
                mergedHist->Write();
                delete mergedHist;
            }
        }

        outFile->Close();
    }

    std::cout << "Done. Output saved in: " << output_dir << std::endl;
}

