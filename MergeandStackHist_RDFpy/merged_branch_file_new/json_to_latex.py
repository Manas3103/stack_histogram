import json
import math

# ============================================================
# Input JSON
# ============================================================

json_file = "yield_values.json"

with open(json_file, "r") as f:
    data = json.load(f)


# ============================================================
# MC processes
# ============================================================

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


# ============================================================
# Output LaTeX file
# ============================================================

with open("yield_tables.tex", "w") as tex:

    for filename, histograms in data.items():

        # Region name
        region = filename.replace("_Yield.root", "")

        total_mc = 0.0
        total_mc_error_squared = 0.0

        data_yield = 0.0
        data_error_squared = 0.0

        process_results = {}

        # ----------------------------------------------------
        # Read processes
        # ----------------------------------------------------

        for process, values in histograms.items():

            integral = values["integral"]

            # Calculate statistical error on integral
            error_squared = sum(
                b["error"] ** 2
                for b in values["bins"]
            )

            integral_error = math.sqrt(error_squared)

            process_results[process] = {
                "yield": integral,
                "error": integral_error
            }

            # MC
            if process in mc_processes:

                total_mc += integral
                total_mc_error_squared += integral_error ** 2

            # Data
            elif process == "data":

                data_yield = integral
                data_error_squared += integral_error ** 2


        total_mc_error = math.sqrt(total_mc_error_squared)
        data_error = math.sqrt(data_error_squared)


        # ====================================================
        # Write LaTeX table
        # ====================================================

        tex.write("\\begin{table}[htbp]\n")
        tex.write("\\centering\n")

        tex.write(
            f"\\caption{{Event yields for the "
            f"{region.replace('_', '\\_')} region. "
            f"The percentage indicates the contribution of each "
            f"MC process to the total MC prediction.}}\n"
        )

        tex.write(
            f"\\label{{tab:{region}_yields}}\n"
        )

        tex.write("\\begin{tabular}{lccc}\n")
        tex.write("\\hline\n")

        tex.write(
            "Process & Yield & Stat. Uncertainty "
            "& Fraction of MC (\\%) \\\\\n"
        )

        tex.write("\\hline\n")


        # ----------------------------------------------------
        # Individual MC processes
        # ----------------------------------------------------

        for process in mc_processes:

            if process not in process_results:
                continue

            yield_value = process_results[process]["yield"]
            error_value = process_results[process]["error"]

            fraction = (
                100.0 * yield_value / total_mc
                if total_mc != 0 else 0.0
            )

            # Escape LaTeX special characters
            latex_process = process.replace("_", "\\_")

            tex.write(
                f"{latex_process} & "
                f"${yield_value:.3f}$ & "
                f"${error_value:.3f}$ & "
                f"${fraction:.2f}$ \\\\\n"
            )


        # ----------------------------------------------------
        # Total MC
        # ----------------------------------------------------

        tex.write("\\hline\n")

        tex.write(
            f"Total MC & "
            f"${total_mc:.3f}$ & "
            f"${total_mc_error:.3f}$ & "
            f"$100.00$ \\\\\n"
        )


        # ----------------------------------------------------
        # Data
        # ----------------------------------------------------

        tex.write(
            f"Data & "
            f"${data_yield:.3f}$ & "
            f"${data_error:.3f}$ & "
            f"-- \\\\\n"
        )

        tex.write("\\hline\n")
        tex.write("\\end{tabular}\n")
        tex.write("\\end{table}\n\n")


print("Created: yield_tables.tex")
