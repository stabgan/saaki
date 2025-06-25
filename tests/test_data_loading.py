import pandas as pd
from pathlib import Path


def test_csv_loading():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "mimic_saaki_final.csv"
    assert csv_path.is_file(), f"CSV file not found: {csv_path}"
    df = pd.read_csv(csv_path)
    assert not df.empty, "Dataframe should have at least one row"
    assert df.shape[1] > 0, "Dataframe should have at least one column"
