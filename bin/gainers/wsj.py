from base import GainerBase
from pathlib import Path
import pandas as pd
import os
import re

class GainerWSJ(GainerBase):
    def __init__(self):
        pass

    def download_html(self):
        print("WSJ html download")
        os.system('sudo google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=5000 https://www.wsj.com/market-data/stocks/us/movers > wsjgainers.html')

    def extract_csv(self):
        print("WSJ csv create")
        raw = pd.read_html(self.html_path)
        raw[0].to_csv(self.csv_path, index=False)

    def normalize_data(self):
        print("WSJ normalize csv")
        df = pd.read_csv(self.csv_path)

        # --- Pick the "company (TICKER)" column ---
        candidates = ["Company", "Name", "Unnamed: 0"]
        comp_col = next((c for c in candidates if c in df.columns), None)

        if comp_col is None:
            comp_col = df.columns[0]
            has_ticker = df[comp_col].astype(str).str.contains(r"\([A-Z.]+\)\s*$")
            if not has_ticker.any():
                for c in df.columns:
                    if df[c].astype(str).str.contains(r"\([A-Z.]+\)\s*$").any():
                        comp_col = c
                        break

        # --- Numeric columns (common WSJ variants) ---
        def pick(names, default=None):
            for n in names:
                if n in df.columns:
                    return n
            return default

        price_col = pick(["Price", "Last", "Last Price"])
        chg_col   = pick(["Chg", "Change", "Change Net"])
        pct_col   = pick(["% Chg", "Change %", "Chg %"])
        vol_col   = pick(["Volume", "Vol", "Vol."])

        if not all([price_col, chg_col, pct_col, vol_col, comp_col]):
            raise ValueError(f"Couldn't find expected columns. Have: {list(df.columns)}")

        # --- Extract symbol + clean company name ---
        rex_symbol = r"\(([A-Z.]+)\)\s*$"
        df["symbol"] = df[comp_col].astype(str).str.extract(rex_symbol, expand=False)

        df["company_name"] = (
            df[comp_col]
            .astype(str)
            .str.replace(r"\s*\([A-Z.]+\)\s*$", "", regex=True)
            .str.strip()
        )

        df = df.dropna(subset=["symbol"]).copy()

        # --- Coerce numerics ---
        def to_float(x):
            s = str(x).strip().replace(",", "").replace("$", "").replace("%", "")
            try:
                return float(s)
            except ValueError:
                return None

        df["price"] = df[price_col].map(to_float)
        df["change"] = df[chg_col].map(to_float)
        df["perc_change"] = df[pct_col].map(to_float)
        df["volume"] = df[vol_col].astype(str).str.strip().str.upper()

        out = df[["symbol", "company_name", "price", "change", "perc_change", "volume"]]
        out.to_csv(self.out_path, index=False)
        return self.out_path


if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 2, "Please pass in one of 'html', 'csv', 'normalize'"
    function = sys.argv[1]
    valid_functions = ['html', 'csv', 'normalize']
    assert function in valid_functions, f"Expected one of {valid_functions} but got {function}"

    gainer = GainerWSJ()
    if function == 'html':
        gainer.download_html()
    elif function == 'csv':
        gainer.extract_csv()
    elif function == 'normalize':
        gainer.normalize_data()
