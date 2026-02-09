# Input / Output directories
INPUT_DIR = "../all_root_file"
OUTPUT_DIR = "merged_branch_file_new"

# Process groups
PROCESS_GROUPS = {
    "DY": [
        "dy_10to50_hist_new.root",
        "dy_m50_hist_new.root"
    ],
    "tt+jets": [
        "ttbar_dilepton_hist_new.root",
        "ttbar_semilep_hist_new.root"
    ],
    "Xy": [
        "zg_ntgc_hist_new.root",
        "tgqb_hist_new.root",
        "wg_10to100_hist_new.root"
    ],
    "VVV": [
        "www_hist_new.root",
        "wwz_hist_new.root",
        "wzz_hist_new.root",
        "zzz_hist_new.root"
    ],
    "t(t)X": [
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
    ],
    "ZZ": [
        "zz_hist_new.root"
    ],
    "WZ": [
        "wz_hist_new.root"
    ],
    "ttZ": [
        "ttz_4to50_hist_new.root",
        "ttz_50_hist_new.root"
    ],
    "tZq": [
        "top_zq_hist_new.root"
    ],
    "data": [
        "All_data_nodup_hist_noNorm.root"
    ]
}

# Optional: manually specify histogram branches
# Leave empty [] to auto-detect from reference file
HISTOGRAM_BRANCHES = []

# Plot output directory
PLOT_OUTPUT_DIR = "merged_branch_file_new/plots"

# MC stack order (controls draw order)
MC_STACK_ORDER = [
    "DY", "tt+jets", "Xy", "VVV", "t(t)X", "ZZ", "WZ", "ttZ", "tZq"
]

# Color map
COLOR_MAP = {
    "DY": 418,
    "tt+jets": 600,
    "Xy": 867,
    "VVV": 880,
    "t(t)X": 921,
    "ZZ": 797,
    "WZ": 856,
    "ttZ": 632,
    "tZq": 416,
}

