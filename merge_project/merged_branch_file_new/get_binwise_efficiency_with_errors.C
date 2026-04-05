#include <TFile.h>
#include <TH1.h>
#include <TKey.h>
#include <TCollection.h>

#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <cmath>

void get_binwise_efficiency_with_errors(const char* filename)
{
    TFile *f = TFile::Open(filename, "READ");
    if (!f || f->IsZombie()) {
        std::cerr << "❌ Cannot open file: " << filename << std::endl;
        return;
    }

    TH1 *h_data = nullptr;
    std::vector<TH1*> mc_hists;

    // ---------------------------------------------------
    // Read histograms
    // ---------------------------------------------------
    TIter next(f->GetListOfKeys());
    TKey *key;

    while ((key = (TKey*)next())) {
        TH1 *h = dynamic_cast<TH1*>(key->ReadObj());
        if (!h) continue;

        std::string name = h->GetName();

        if (name == "data") {
            h_data = h;
        } else {
            mc_hists.push_back(h);
        }
    }

    if (!h_data || mc_hists.empty()) {
        std::cerr << "❌ Missing data or MC histograms\n";
        return;
    }

    int nbins = h_data->GetNbinsX();

    // ---------------------------------------------------
    // Header
    // ---------------------------------------------------
    std::cout << "\n=== Bin-wise Data/MC ratio with statistical uncertainties ===\n\n";

    std::cout
        << std::setw(4)  << "Bin"
        << std::setw(12) << "pT_low"
        << std::setw(12) << "pT_high"
        << std::setw(12) << "Data"
        << std::setw(12) << "σ(Data)"
        << std::setw(12) << "MC"
        << std::setw(12) << "σ(MC)"
        << std::setw(14) << "Data/MC"
        << std::setw(14) << "σ(Data/MC)"
        << std::endl;

    std::cout << std::string(114, '-') << std::endl;

    // ---------------------------------------------------
    // Loop over bins
    // ---------------------------------------------------
    for (int i = 1; i <= nbins; ++i) {

        double data_bin = h_data->GetBinContent(i);
        double data_err = std::sqrt(data_bin);  // Poisson

        double mc_bin = 0.0;
        double mc_err2 = 0.0;  // sum of errors^2

        for (auto hmc : mc_hists) {
            mc_bin  += hmc->GetBinContent(i);
            mc_err2 += std::pow(hmc->GetBinError(i), 2);
        }

        double mc_err = std::sqrt(mc_err2);

        double ratio = 0.0;
        double ratio_err = 0.0;

        if (mc_bin > 0 && data_bin > 0) {
            ratio = data_bin / mc_bin;

            ratio_err = ratio * std::sqrt(
                std::pow(data_err / data_bin, 2) +
                std::pow(mc_err  / mc_bin,  2)
            );
        }

        // ---------------------------------------------------
        // Print row
        // ---------------------------------------------------
        std::cout
            << std::setw(4)  << i
            << std::setw(12) << std::fixed << std::setprecision(1)
            << h_data->GetBinLowEdge(i)
            << std::setw(12)
            << h_data->GetBinLowEdge(i+1)
            << std::setw(12) << std::setprecision(0)
            << data_bin
            << std::setw(12) << std::setprecision(1)
            << data_err
            << std::setw(12) << std::setprecision(1)
            << mc_bin
            << std::setw(12)
            << mc_err
            << std::setw(14) << std::setprecision(3)
            << ratio
            << std::setw(14)
            << ratio_err
            << std::endl;
    }

    f->Close();
}

