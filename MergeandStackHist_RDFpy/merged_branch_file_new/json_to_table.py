import json
import math

# ============================================================
# Input JSON
# ============================================================

json_file = "yield_values.json"

with open(json_file, "r") as f:
    data = json.load(f)


# ============================================================
# Define processes
# ============================================================

# MC processes
mc_processes = [
    "DY",
    "tt+jets",
    "Xy",
    "VVV",
    "t(t)X",
    "ZZ",
    "WZ",
    "ttZ",
    "tZq"
]

data_process = "data"


# ============================================================
# Store results
# ============================================================

results = {}


for filename, histograms in data.items():

    # Convert filename to region name
    region = filename.replace("_Yield.root", "")

    total_mc = 0.0
    total_mc_error_squared = 0.0

    data_yield = 0.0
    data_error_squared = 0.0

    process_results = {}

    # --------------------------------------------------------
    # Loop over all histograms/processes
    # --------------------------------------------------------

    for process, values in histograms.items():

        integral = values["integral"]

        # Calculate error on integral
        error_squared = 0.0

        for bin_info in values["bins"]:
            error_squared += bin_info["error"] ** 2

        integral_error = math.sqrt(error_squared)

        process_results[process] = {
            "yield": integral,
            "error": integral_error
        }

        # ----------------------------------------------------
        # Add MC
        # ----------------------------------------------------

        if process in mc_processes:

            total_mc += integral
            total_mc_error_squared += integral_error ** 2

        # ----------------------------------------------------
        # Data
        # ----------------------------------------------------

        elif process == data_process:

            data_yield = integral
            data_error_squared += integral_error ** 2


    # Total MC error
    total_mc_error = math.sqrt(total_mc_error_squared)

    # Data error
    data_error = math.sqrt(data_error_squared)

    # Data / MC
    if total_mc != 0:
        data_mc_ratio = data_yield / total_mc
    else:
        data_mc_ratio = 0.0

    # Data - MC
    difference = data_yield - total_mc

    # Combined uncertainty on Data-MC
    difference_error = math.sqrt(
        data_error ** 2 + total_mc_error ** 2
    )

    results[region] = {
        "processes": process_results,
        "total_mc": total_mc,
        "total_mc_error": total_mc_error,
        "data": data_yield,
        "data_error": data_error,
        "data_mc_ratio": data_mc_ratio,
        "data_minus_mc": difference,
        "data_minus_mc_error": difference_error
    }

# ============================================================
# Cross-check:
# Sum of eee + eeu + uue + uuu vs ThreeLRegion
# ============================================================

exclusive_regions = [
    "eee_ThreeLRegion",
    "eeu_ThreeLRegion",
    "uue_ThreeLRegion",
    "uuu_ThreeLRegion"
]

inclusive_region = "ThreeLRegion"


print("\n\n")
print("=" * 110)
print("CROSS-CHECK: ThreeLRegion vs Sum of Exclusive Flavor Regions")
print("=" * 110)


# Check that all required regions exist
missing_regions = [
    region for region in [inclusive_region] + exclusive_regions
    if region not in results
]

if missing_regions:

    print("\nWARNING: The following regions are missing from the JSON:")

    for region in missing_regions:
        print(f"  - {region}")

else:

    # --------------------------------------------------------
    # Inclusive ThreeLRegion
    # --------------------------------------------------------

    inclusive_mc = results[inclusive_region]["total_mc"]
    inclusive_mc_error = results[inclusive_region]["total_mc_error"]

    inclusive_data = results[inclusive_region]["data"]
    inclusive_data_error = results[inclusive_region]["data_error"]


    # --------------------------------------------------------
    # Sum exclusive regions
    # --------------------------------------------------------

    summed_mc = 0.0
    summed_mc_error_squared = 0.0

    summed_data = 0.0
    summed_data_error_squared = 0.0


    for region in exclusive_regions:

        summed_mc += results[region]["total_mc"]

        summed_mc_error_squared += (
            results[region]["total_mc_error"] ** 2
        )

        summed_data += results[region]["data"]

        summed_data_error_squared += (
            results[region]["data_error"] ** 2
        )


    summed_mc_error = math.sqrt(
        summed_mc_error_squared
    )

    summed_data_error = math.sqrt(
        summed_data_error_squared
    )


    # --------------------------------------------------------
    # Differences
    # --------------------------------------------------------

    mc_difference = summed_mc - inclusive_mc

    data_difference = summed_data - inclusive_data


    # --------------------------------------------------------
    # Relative differences
    # --------------------------------------------------------

    if inclusive_mc != 0:
        mc_relative_difference = (
            100.0 * mc_difference / inclusive_mc
        )
    else:
        mc_relative_difference = 0.0


    if inclusive_data != 0:
        data_relative_difference = (
            100.0 * data_difference / inclusive_data
        )
    else:
        data_relative_difference = 0.0


    # --------------------------------------------------------
    # Matching criteria
    # --------------------------------------------------------

    tolerance = 1e-6

    mc_match = abs(mc_difference) < tolerance
    data_match = abs(data_difference) < tolerance


    # ========================================================
    # Print results
    # ========================================================

    print("\nMC CROSS-CHECK")
    print("-" * 110)

    print(
        f"{'ThreeLRegion MC':<30}"
        f"{inclusive_mc:>15.3f} +/- "
        f"{inclusive_mc_error:<10.3f}"
    )

    print(
        f"{'Sum of 4 exclusive MC':<30}"
        f"{summed_mc:>15.3f} +/- "
        f"{summed_mc_error:<10.3f}"
    )

    print(
        f"{'Difference (Sum - ThreeL)':<30}"
        f"{mc_difference:>15.6f}"
    )

    print(
        f"{'Relative difference':<30}"
        f"{mc_relative_difference:>14.6f}%"
    )

    if mc_match:
        print("\nMC RESULT: MATCH")
    else:
        print("\nMC RESULT: DOES NOT MATCH")


    print("\nDATA CROSS-CHECK")
    print("-" * 110)

    print(
        f"{'ThreeLRegion Data':<30}"
        f"{inclusive_data:>15.3f} +/- "
        f"{inclusive_data_error:<10.3f}"
    )

    print(
        f"{'Sum of 4 exclusive Data':<30}"
        f"{summed_data:>15.3f} +/- "
        f"{summed_data_error:<10.3f}"
    )

    print(
        f"{'Difference (Sum - ThreeL)':<30}"
        f"{data_difference:>15.6f}"
    )

    print(
        f"{'Relative difference':<30}"
        f"{data_relative_difference:>14.6f}%"
    )

    if data_match:
        print("\nDATA RESULT: MATCH")
    else:
        print("\nDATA RESULT: DOES NOT MATCH")


    print("\n" + "=" * 110)
# ============================================================
# Print table
# ============================================================

print()

header = (
    f"{'Region':<30}"
    f"{'Total MC':>20}"
    f"{'Data':>20}"
    f"{'Data/MC':>12}"
    f"{'Data-MC':>20}"
)

print(header)
print("=" * len(header))


for region, result in results.items():

    mc = result["total_mc"]
    mc_err = result["total_mc_error"]

    dat = result["data"]
    dat_err = result["data_error"]

    ratio = result["data_mc_ratio"]

    diff = result["data_minus_mc"]
    diff_err = result["data_minus_mc_error"]

    print(
        f"{region:<30}"
        f"{mc:>10.2f} +/- {mc_err:<7.2f}"
        f"{dat:>10.2f} +/- {dat_err:<7.2f}"
        f"{ratio:>12.3f}"
        f"{diff:>10.2f} +/- {diff_err:<7.2f}"
    )


# ============================================================
# Print individual process yields
# ============================================================

# print("\n\nINDIVIDUAL PROCESS YIELDS")
# print("=" * 100)

# for region, result in results.items():

#     print(f"\nRegion: {region}")
#     print("-" * 70)

#     for process, values in result["processes"].items():

#         print(
#             f"{process:<15}"
#             f"{values['yield']:>15.3f} +/- "
#             f"{values['error']:<10.3f}"
#         )

#     print(
#         f"{'Total MC':<15}"
#         f"{result['total_mc']:>15.3f} +/- "
#         f"{result['total_mc_error']:<10.3f}"
#     )

#     print(
#         f"{'Data':<15}"
#         f"{result['data']:>15.3f} +/- "
#         f"{result['data_error']:<10.3f}"
#     )

# ============================================================
# Print individual process yields and MC composition
# ============================================================

print("\n\nINDIVIDUAL PROCESS YIELDS")
print("=" * 100)

for region, result in results.items():

    print(f"\nRegion: {region}")
    print("-" * 100)

    print(
        f"{'Process':<15}"
        f"{'Yield':>15}"
        f"{'Stat. Error':>15}"
        f"{'% of Total MC':>18}"
    )

    print("-" * 100)

    # --------------------------------------------------------
    # Individual MC processes
    # --------------------------------------------------------

    for process, values in result["processes"].items():

        # Skip data here to avoid printing it twice
        if process == "data":
            continue

        process_yield = values["yield"]
        process_error = values["error"]

        # Fraction of total MC
        if result["total_mc"] != 0:
            fraction = 100.0 * process_yield / result["total_mc"]
        else:
            fraction = 0.0

        print(
            f"{process:<15}"
            f"{process_yield:>15.3f}"
            f"{process_error:>15.3f}"
            f"{fraction:>17.2f}%"
        )

    print("-" * 100)

    # --------------------------------------------------------
    # Total MC
    # --------------------------------------------------------

    print(
        f"{'Total MC':<15}"
        f"{result['total_mc']:>15.3f}"
        f"{result['total_mc_error']:>15.3f}"
        f"{100.0:>17.2f}%"
    )

    # --------------------------------------------------------
    # Data — printed only once
    # --------------------------------------------------------

    print(
        f"{'Data':<15}"
        f"{result['data']:>15.3f}"
        f"{result['data_error']:>15.3f}"
        f"{'--':>18}"
    )
