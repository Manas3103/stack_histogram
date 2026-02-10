from histogram_merger import HistogramMerger
from stack_plotter import StackPlotter
"""
def main():
    print("Starting histogram merge job...")
    merger = HistogramMerger()
    merger.run()
    print("All done!")
"""

def main():
    print("\n--- Starting Histogram Merge Job ---")
    
    merger = HistogramMerger(partial_tag=True)
   # merger = HistogramMerger()
    merged_files = merger.run()

    print("\n--- Generating Stack Plots ---")

    for root_file in merged_files:
        try:
            plotter = StackPlotter(root_file)
            plotter.run()
        except Exception as e:
            print(f"Skipping {root_file}: {e}")

    print("\n--- All Done ---")

if __name__ == "__main__":
    main()

