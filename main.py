from src.experiment import run_experiment
import os
import sys

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(BASE_DIR, "data", "raw")

    min_util = 0.05
    max_len = 5

    datasets = [
        "Synthetic3k.txt",
        "Synthetic8k.txt",
        "Kosarak10k.txt",
        "Bible.txt"
    ]

    if len(sys.argv) > 1:
        datasets = [sys.argv[1]]

    for ds in datasets:
        dataset_path = os.path.join(data_dir, ds)

        print(f"\n🚀 Running: {ds}")

        run_experiment(
            dataset=dataset_path,
            min_util=min_util,
            max_len=max_len
        )