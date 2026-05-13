import ROOT

# Input / Output directories
INPUT_DIR = "2024_root_files"
OUTPUT_DIR = "merged_branch_file_new"

# Process groups
PROCESS_GROUPS = {
    "DY": [
        "DYto_2E2Jet_part10_skimed_hist.root",
        "DYto_2E2Jet_part1_skimed_hist.root",
        "DYto_2E2Jet_part2_skimed_hist.root",
        "DYto_2E2Jet_part3_skimed_hist.root",
        "DYto_2E2Jet_part4_skimed_hist.root",
        "DYto_2E2Jet_part5_skimed_hist.root",
        "DYto_2E2Jet_part6_skimed_hist.root",
        "DYto_2E2Jet_part7_skimed_hist.root",
        "DYto_2E2Jet_part8_skimed_hist.root",
        "DYto_2E2Jet_part9_skimed_hist.root",
        "DYto_2Mu2Jet_part1_skimed_hist.root",
        "DYto_2Mu2Jet_part2_skimed_hist.root",
        "DYto_2Mu2Jet_part3_skimed_hist.root",
        "DYto_2Mu2Jet_part4_skimed_hist.root",
        "DYto_2Mu2Jet_part5_skimed_hist.root",
        "DYto_2Mu2Jet_part6_skimed_hist.root",
        "DYto_2Mu2Jet_part7_skimed_hist.root",
        "DYto_2Mu2Jet_part8_skimed_hist.root",
        "DYto_2Mu2Jet_part9_skimed_hist.root",
        "DYto_2Tau2Jet_part10_skimed_hist.root",
        "DYto_2Tau2Jet_part1_skimed_hist.root",
        "DYto_2Tau2Jet_part2_skimed_hist.root",
        "DYto_2Tau2Jet_part3_skimed_hist.root",
        "DYto_2Tau2Jet_part4_skimed_hist.root",
        "DYto_2Tau2Jet_part5_skimed_hist.root",
        "DYto_2Tau2Jet_part6_skimed_hist.root",
        "DYto_2Tau2Jet_part7_skimed_hist.root",
        "DYto_2Tau2Jet_part8_skimed_hist.root",
        "DYto_2Tau2Jet_part9_skimed_hist.root",
        "DYto2Tau-2Jets_M2L10-50_hist.root",
        "DYto2Mu-2Jets_M2L-10to50_hist.root",
        "DYto2E-2Jets_M2L-10to50_hist.root"

    ],
    "tt+jets": [
        "ttbar_semilep_part1_skimed_hist.root",
        "ttbar_semilep_part2_skimed_hist.root",
        "ttbar_semilep_part3_skimed_hist.root",
        "ttbar_semilep_part4_skimed_hist.root",
        "ttbar_semilep_part5_skimed_hist.root",
        "ttbar_semilep_part6_skimed_hist.root",
        "ttbar_semilep_part7_skimed_hist.root",
        "ttbar_semilep_part8_skimed_hist.root",

        # dilepton parts
        "ttbar_dilepton_part1_skimed_hist.root",
        "ttbar_dilepton_part2_skimed_hist.root",
        "ttbar_dilepton_part3_skimed_hist.root",
        "ttbar_dilepton_part4_skimed_hist.root",
        "ttbar_dilepton_part5_skimed_hist.root",
        "ttbar_dilepton_part6_skimed_hist.root",
        "ttbar_dilepton_part7_skimed_hist.root",
        "ttbar_dilepton_part8_skimed_hist.root",
    ],
    "Xy": [
#        "zg_ntgc_hist.root",
        "tgqb_hist.root",
        "wg_1jet_part1_skimed_hist.root",
        "wg_1jet_part2_skimed_hist.root",
        "wg_1jet_part3_skimed_hist.root",
        "wg_1jet_part4_skimed_hist.root",
        "wg_1jet_part5_skimed_hist.root",
        "wg_1jet_part6_skimed_hist.root",
        "wg_1jet_part7_skimed_hist.root",
        "wg_1jet_part8_skimed_hist.root",
        "wg_1jet_part9_skimed_hist.root",
        "wg_1jet_part10_skimed_hist.root",
        "wg_1jet_part11_skimed_hist.root",
        "wg_1jet_part12_skimed_hist.root",
        "wg_1jet_part13_skimed_hist.root",
        "wg_1jet_part14_skimed_hist.root",
        "wg_1jet_part15_skimed_hist.root",
        "wg_1jet_part16_skimed_hist.root",
        "wg_1jet_part17_skimed_hist.root",
        "wg_1jet_part18_skimed_hist.root",
        "wg_1jet_part19_skimed_hist.root",
        "wg_1jet_part20_skimed_hist.root",
    ],
    "VVV": [
        "www_hist.root",
        "wwz_hist.root",
        "wzz_hist.root",
        "zzz_hist.root"
    ],
    "t(t)X": [
        "tbarWplus_2l2nu_hist.root",
        "tWminus_2l2nu_hist.root",
#        "tth_non2b_hist.root",
        "ttwh_hist.root",
        "ttww_hist.root",
#        "ttzh_hist.root",
        "ttzz_hist.root",
        "tttt_hist.root",
#        "thq_hist.root",
        "tbarb_lmin_hist.root",
        "tbbar_lplus_hist.root",
#        "thw_hist.root"
    ],
    "ZZ": [
        "ggh_zz_4l_hist.root",
        "vbfh_zz_4l_hist.root",
        "GluGlu2zto4Tau_hist.root",
        "GluGlu2zto4Mu_hist.root",
        "GluGlu2zto4E_hist.root",
        "GluGlu2zto2Mu2Tau_hist.root",
        "GluGlu2zto2E2Tau_hist.root",
        "GluGlu2zto2E2Mu_hist.root",
        "wmh_zz_4l_hist.root",
        "wph_zz_4l_hist.root",
        "zz_4l_part1_skimed_hist.root",
        "zz_4l_part2_skimed_hist.root",
        "zz_4l_part3_skimed_hist.root",
        "zz_4l_part4_skimed_hist.root",
        "zz_4l_part5_skimed_hist.root",
        "zz_4l_part6_skimed_hist.root",
        "zz_4l_part7_skimed_hist.root",
        "zz_4l_part8_skimed_hist.root",
    ],
    "WZ": [
        "wz_3lnu_part1_skimed_hist.root",
        "wz_3lnu_part2_skimed_hist.root",
        "wz_3lnu_part3_skimed_hist.root",
        "wz_3lnu_part4_skimed_hist.root",
        "wz_3lnu_part5_skimed_hist.root",
        "wz_3lnu_part6_skimed_hist.root",
        "wz_3lnu_part7_skimed_hist.root",
        "wz_3lnu_part8_skimed_hist.root",
    ],
    "ttZ": [
        "ttz_4to50_hist.root",
        "ttz_50_hist.root"
    ],
    "tZq": [
        "top_zq_hist.root"
    ],
    "data": [
#        "Era_C_merged_nodup_py_hist.root",
#        "Era_D_merged_nodup_py_hist.root",
#        "Era_E_merged_nodup_py_hist.root",
#        "Era_F_merged_nodup_py_hist.root",
#       "Era_G_merged_nodup_hist.root",
        "Era_G_merged_nodup_py_hist.root",
#        "Era_H_merged_nodup_hist.root",
#        "Era_I_merged_nodup_py_hist.root"
    ]

}

# Process groups
PROCESS_GROUPS_FULL = {
    "DY": [
        "dy_10to50_hist.root",
        "dy_m50_hist.root"
    ],

    "tt+jets": [
        "ttbar_dilepton_hist.root",
        "ttbar_semilep_hist.root"
    ],

    "Xy": [
        "zg_ntgc_hist.root",
        "tgqb_hist.root",
        "wg_10to100_hist.root"
    ],

    "VVV": [
        "www_hist.root",
        "wwz_hist.root",
        "wzz_hist.root",
        "zzz_hist.root"
    ],

    "t(t)X": [
        "tth_non2b_hist.root",
        "ttwh_hist.root",
        "ttww_hist.root",
        "ttzh_hist.root",
        "ttzz_hist.root",
        "tttt_hist.root",
        "thq_hist.root",
        "tbarb_lmin_hist.root",
        "tbbar_lplus_hist.root",
        "thw_hist.root"
    ],

    "ZZ": [
        "ggh_zz_4l_hist.root",
        "gg_zz_2mu2tau_hist.root",
        "gg_zz_2e2tau_hist.root",
        "gg_zz_2e2mu_hist.root",
        "gg_zz_4e_hist.root",
        "gg_zz_4mu_hist.root",
        "vbfh_zz_4l_hist.root",
        "wmh_zz_4l_hist.root",
        "wph_zz_4l_hist.root",
        "zz_hist.root"
    ],

    "WZ": [
        "wz_hist.root"
    ],

    "ttZ": [
        "ttz_4to50_hist.root",
        "ttz_50_hist.root"
    ],

    "tZq": [
        "top_zq_hist.root"
    ],

    "data": [
        "Era_C_merged_nodup_hist.root"
        "Era_D_merged_nodup_hist.root"
        #"Era_E_merged_nodup_hist.root"
        #"Era_F_merged_nodup_hist.root"
        #"Era_G_merged_nodup_hist.root"
        #"Era_H_merged_nodup_hist.root"
        #"Era_I_merged_nodup_hist.root"
    ]
}


# Optional: manually specify histogram branches
# Leave empty [] to auto-detect from reference file
HISTOGRAM_BRANCHES = []

# Plot output directory
PLOT_OUTPUT_DIR = "merged_branch_file_new/plots"
"""
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
"""


COLOR_MAP = {
    "tZq": ROOT.kRed - 7,
    "ttZ": ROOT.kGreen - 7,
    "WZ": ROOT.kAzure - 9,
    "ZZ": ROOT.kOrange - 2,
    "t(t)X": ROOT.kViolet - 7,
    "VVV": ROOT.kPink - 3,
    "Xy": ROOT.kYellow - 7,
    "tt+jets": ROOT.kGreen + 1,
    "DY": ROOT.kBlue - 6,
}

MC_STACK_ORDER = [
    "DY", "tt+jets", "Xy", "VVV", "t(t)X",
    "ZZ", "WZ", "ttZ", "tZq"
]

