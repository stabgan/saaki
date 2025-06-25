"""Simple exploratory script for the SA-AKI dataset."""

import os
import pandas as pd


def main() -> None:
    """Load the dataset and print the first few rows."""
    # Compute the path to the CSV relative to this file so the script works
    # no matter where it is executed from.
    here = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(here, "..", "data", "mimic_saaki_final.csv")

    df = pd.read_csv(csv_path)
    print(df.head())


if __name__ == "__main__":
    main()
