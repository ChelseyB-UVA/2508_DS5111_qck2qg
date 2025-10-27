from base import GainerBase
from pathlib import Path
import os
import re
import pandas as pd

class GainerYahoo(GainerBase):
    def __init__(self, html_path="ygainers.html", csv_path="ygainers.csv", out_path="ygainers_normalized.csv"):
        self.html_path = Path(html_path)
        self.csv_path = Path(csv_path)
        self.out_path = Path(out_path)

    def download_html(self):
        print("Yahoo html download")
        # Keep your original style (os.system and sudo); redirect into self.html_path
        os.system(
            f"sudo google-chrome-stable --headless --disable-gpu --dump-dom "
            f"--no-sandbox --timeout=5000 "
            f"'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200' "
            f"> {self.html_path}"
        )

    def extract_csv(self):
        print("Yahoo csv create")
        tables = pd.read_html(self.html_path)
        if not tables:
            raise ValueError("No tables found in Yahoo HTML.")
        # Same idea as your original: take the first table
        tables[0].to_csv(self.csv_path, index=False)

    def normalize_data(self):
        """Normalize a Yahoo Finance gainers CSV to a standard schema and write to self.out_path."""
        print("Yahoo normalize csv")
        df = pd.read_csv(self.csv_path)

        # Helpers (kept simple but robust)
        def _to_float(x):
            s = str(x).strip().replace(",", "").replace("$", "").replace("%", "")
            if s in {"", "nan", "None", "—", "-", "–"}:
                return None
            try:
                return float(s)
            except ValueError:
                return None

        vol_re = re.compile(r"^\s*([0-9]*\.?[0-9]+)\s*([KMB]?)\s*$", re.IGNORECASE)
        mult = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}

        def _parse_volume(v):
            s = str(v).strip().replace(",", "")
            if s in {"", "nan", "None"}:
                return None
            m = vol_re.match(s)
            if not m:
                try:
                    return int(float(s))
                except ValueError:
                    return None
            num = float(m.group(1))
            suf = m.group(2).upper()
            return int(num * mult.get(suf, 1))

        # Build normalized output
        out = pd.DataFrame()
        out["symbol"] = df["Symbol"].astype(str).str.strip().str.upper() if "Symbol" in df.columns else None
        out["company_name"] = df["Name"].astype(str).str.strip() if "Name" in df.columns else None

        # Price / Change / % Change: use columns if present, else parse from "Price" blob like "7.93 +3.40 (75.06%)"
        if "Price" in df.columns:
            out["price"] = df["Price"].map(_to_float)
        else:
            out["price"] = None

        if "Change" in df.columns:
            out["change"] = df["Change"].map(_to_float)
        else:
            out["change"] = None

        if "% Change" in df.columns:
            out["perc_change"] = df["% Change"].map(_to_float)
        elif "%Change" in df.columns:
            out["perc_change"] = df["%Change"].map(_to_float)
        else:
            out["perc_change"] = None

        # Fallback parse from combined "Price" text
        if (out["change"].isna().all() or out["perc_change"].isna().all()) and "Price" in df.columns:
            s = df["Price"].astype(str)
            parsed_price = s.str.extract(r"^\s*([-+]?\d+(?:\.\d+)?)")[0].map(_to_float)
            parsed_change = s.str.extract(r"^\s*[-+]?\d+(?:\.\d+)?\s+([-+]?\d+(?:\.\d+)?)")[0].map(_to_float)
            parsed_pct = s.str.extract(r"\(([-+]?\d+(?:\.\d+)?)%")[0].map(_to_float)
            out["price"] = out["price"].fillna(parsed_price)
            out["change"] = out["change"].fillna(parsed_change)
            out["perc_change"] = out["perc_change"].fillna(parsed_pct)

        # Volume
        if "Volume" in df.columns:
            out["volume"] = df["Volume"].map(_parse_volume)
        else:
            out["volume"] = None

        # Final column order
        out = out[["symbol", "company_name", "price", "change", "perc_change", "volume"]]
        out.to_csv(self.out_path, index=False)
        return self.out_path

