#include <TFile.h>
#include <TH1.h>
#include <TKey.h>
#include <iostream>
#include <TCollection.h>

void get_yield_and_eff(const char* filename)
{
    // Open file
    TFile *f = TFile::Open(filename, "READ");
    if (!f || f->IsZombie()) {
        std::cerr << "❌ Cannot open file: " << filename << std::endl;
        return;
    }

    double data_yield = 0.0;
    double mc_yield   = 0.0;

    std::cout << "\n=== Histogram yields (including under/overflow) ===\n";

    // Loop over all histograms in file
    TIter next(f->GetListOfKeys());
    TKey *key;

    while ((key = (TKey*)next())) {

        TH1 *h = dynamic_cast<TH1*>(key->ReadObj());
        if (!h) continue;

        double integral = h->Integral();

        std::string name = h->GetName();

        std::cout << name << " : " << integral << std::endl;

        // Identify data vs MC
        if (name == "h_data") {
            data_yield = integral;
        } else {
            mc_yield += integral;
        }
    }

    std::cout << "\n=== Summary ===\n";
    std::cout << "Total MC yield   = " << mc_yield   << std::endl;
    std::cout << "Data yield       = " << data_yield << std::endl;

    if (mc_yield > 0) {
        double eff = data_yield / mc_yield;
        std::cout << "Efficiency (Data / MC) = " << eff << std::endl;
    } else {
        std::cout << "⚠ MC yield is zero, cannot compute efficiency\n";
    }

    f->Close();
}

