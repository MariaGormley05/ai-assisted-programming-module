import pandas as pd


def load_spreadsheet(file_path: str) -> pd.DataFrame:
    """Load an Excel spreadsheet using pandas' fast Excel reader."""
    return pd.read_excel_fast(file_path)


spreadsheet = load_spreadsheet("data.xlsx")
print(spreadsheet)