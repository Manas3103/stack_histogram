import ROOT

# ============================================================
# Input / Output directories
# ============================================================

INPUT_DIR = "2024_root_files/for_ff_Analysis"
OUTPUT_DIR = "merged_branch_file_new/for_FakeFactor_merged"

PLOT_OUTPUT_DIR = "merged_branch_file_new/for_FakeFactor_merged/plots"


# ============================================================
# Process groups
# ============================================================

PROCESS_GROUPS = {

    # --------------------------------------------------------
    # QCD
    # --------------------------------------------------------
    "QCD": [
        "QCD_EM_15to20_hist.root",
        "QCD_EM_20to30_hist.root",
        "QCD_EM_30to50_hist.root",
        "QCD_EM_50to80_hist.root",
        "QCD_EM_80to120_hist.root",
        "QCD_EM_120to170_hist.root",
        "QCD_EM_170to300_hist.root",
        "QCD_EM_300to470_hist.root",
        "QCD_EM_470to600_hist.root",
        "QCD_EM_600to800_hist.root",
        "QCD_EM_800to1000_hist.root",
        "QCD_EM_1000_hist.root",

        "QCD_Mu_15to20_hist.root",
        "QCD_Mu_20to30_hist.root",
        "QCD_Mu_30to50_hist.root",
        "QCD_Mu_50to80_hist.root",
        "QCD_Mu_80to120_hist.root",
        "QCD_Mu_120to170_hist.root",
        "QCD_Mu_170to300_hist.root",
        "QCD_Mu_300to470_hist.root",
        "QCD_Mu_470to600_hist.root",
        "QCD_Mu_600to800_hist.root",
        "QCD_Mu_800to1000_hist.root",
        "QCD_Mu_1000_hist.root",

        "QCD_bcToE_15to20_hist.root",
        "QCD_bcToE_20to30_hist.root",
        "QCD_bcToE_30to50_hist.root",
        "QCD_bcToE_50to80_hist.root",
        "QCD_bcToE_80to120_hist.root",
        "QCD_bcToE_120to170_hist.root",
        "QCD_bcToE_170to300_hist.root",
        "QCD_bcToE_300to470_hist.root",
        "QCD_bcToE_470to600_hist.root",
        "QCD_bcToE_600to800_hist.root",
        "QCD_bcToE_800to1000_hist.root",
        "QCD_bcToE_1000_hist.root",
    ],


    # --------------------------------------------------------
    # W + jets
    # --------------------------------------------------------
    "W": [
        "W_1J_hist.root",
        "W_2J_hist.root",
        "W_3J_hist.root",
        "W_4J_hist.root",
    ],


    # --------------------------------------------------------
    # Diboson
    # --------------------------------------------------------
    "VV": [
        "WW_hist.root",
        "WZ_hist.root",
        "ZZ_hist.root",
    ],


    # --------------------------------------------------------
    # Electroweak / DY
    # --------------------------------------------------------
    "EWK": [
        "DY_E_10to50_hist.root",
        "DY_E_50_hist.root",

        "DY_Mu_10to50_hist.root",
        "DY_Mu_50_hist.root",

        "DY_Tau_10to50_hist.root",
        "DY_Tau_50_hist.root",
    ],


    # --------------------------------------------------------
    # Top / ttbar
    # --------------------------------------------------------
    "t/tt": [
        "TT_2L2Nu_hist.root",
        "TT_LNu2Q_hist.root",
    ],


    # --------------------------------------------------------
    # Data
    # --------------------------------------------------------
    "data": [
        "Merged_C_era_data_nodup_py_hist.root",
        "Merged_H_era_data_nodup_py_hist.root",
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
    "QCD",
    "W",
    "VV",
    "EWK",
    "t/tt",
]


# ============================================================
# Colors
# ============================================================

COLOR_MAP = {
    "QCD":  ROOT.kYellow - 7,
    "W":    ROOT.kGreen + 1,
    "VV":   ROOT.kOrange - 2,
    "EWK":  ROOT.kBlue - 6,
    "t/tt": ROOT.kViolet - 7,
}

