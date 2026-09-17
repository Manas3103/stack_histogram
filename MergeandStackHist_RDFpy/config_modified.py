import ROOT

# ============================================================
# Input / Output directories
# ============================================================

INPUT_DIR = "2024_root_files"
OUTPUT_DIR = "merged_branch_file_new"

PLOT_OUTPUT_DIR = "merged_branch_file_new/plots"


# ============================================================
# Process groups
# ============================================================

PROCESS_GROUPS = {

    # --------------------------------------------------------
    # Drell-Yan
    # --------------------------------------------------------
    "DY": [
        "DYto_2E2Jet_hist.root",
        "DYto_2Mu2Jet_hist.root",
        "DYto_2Tau2Jet_hist.root",

        "DYto2E-2Jets_M2L-10to50_hist.root",
        "DYto2Mu-2Jets_M2L-10to50_hist.root",
        "DYto2Tau-2Jets_M2L10-50_hist.root",
    ],


    # --------------------------------------------------------
    # tt + jets
    # --------------------------------------------------------
    "tt+jets": [
        "ttbar_dilepton_hist.root",
        "ttbar_semilep_hist.root",
    ],


    # --------------------------------------------------------
    # X + gamma / single-top-associated processes
    # --------------------------------------------------------
    "Xy": [
        "tgqb_hist.root",
        "wg_1jet_hist.root",
    ],


    # --------------------------------------------------------
    # Triple vector boson
    # --------------------------------------------------------
    "VVV": [
        "www_hist.root",
        "wwz_hist.root",
        "wzz_hist.root",
        "zzz_hist.root",
    ],


    # --------------------------------------------------------
    # ttX and other top-associated processes
    # --------------------------------------------------------
    "t(t)X": [
        "tbarWplus_2l2nu_hist.root",
        "tWminus_2l2nu_hist.root",

        "tth_non2b_hist.root",

        "ttwh_hist.root",
        "ttww_hist.root",
        "ttwz_hist.root",
        "ttzz_hist.root",
        "tttt_hist.root",

        "tbarb_lmin_hist.root",
        "tbbar_lplus_hist.root",
    ],


    # --------------------------------------------------------
    # ZZ / Higgs -> ZZ
    # --------------------------------------------------------
    "ZZ": [
        "ggh_zz_4l_hist.root",
        "vbfh_zz_4l_hist.root",
        "wmh_zz_4l_hist.root",
        "wph_zz_4l_hist.root",

        "GluGlu2zto4Tau_hist.root",
        "GluGlu2zto4Mu_hist.root",
        "GluGlu2zto4E_hist.root",

        "GluGlu2zto2Mu2Tau_hist.root",
        "GluGlu2zto2E2Tau_hist.root",
        "GluGlu2zto2E2Mu_hist.root",

        "zz_hist.root",
    ],


    # --------------------------------------------------------
    # WZ
    # --------------------------------------------------------
    "WZ": [
        "wz_hist.root",
    ],


    # --------------------------------------------------------
    # ttZ
    # --------------------------------------------------------
    "ttZ": [
        "ttz_4to50_hist.root",
        "ttz_50_hist.root",
    ],


    # --------------------------------------------------------
    # tZq signal
    # --------------------------------------------------------
    "tZq": [
        "top_zq_hist.root",
    ],


    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------
    "data": [
        "Merged_H_era_data_nodup_py_hist.root",
        "Merged_C_era_data_nodup_py_hist.root",
    ],
}


# ============================================================
# Optional: manually specify histogram branches
#
# Leave empty [] to auto-detect from reference file
# ============================================================

HISTOGRAM_BRANCHES = []


# ============================================================
# MC stack order
# ============================================================

MC_STACK_ORDER = [
    "DY",
    "tt+jets",
    "Xy",
    "VVV",
    "t(t)X",
    "ZZ",
    "WZ",
    "ttZ",
    "tZq",
]


# ============================================================
# Colors
# ============================================================

COLOR_MAP = {
    "tZq":    ROOT.kRed - 7,
    "ttZ":    ROOT.kGreen - 7,
    "WZ":     ROOT.kAzure - 9,
    "ZZ":     ROOT.kOrange - 2,
    "t(t)X":  ROOT.kViolet - 7,
    "VVV":    ROOT.kPink - 3,
    "Xy":     ROOT.kYellow - 7,
    "tt+jets": ROOT.kGreen + 1,
    "DY":     ROOT.kBlue - 6,
}
