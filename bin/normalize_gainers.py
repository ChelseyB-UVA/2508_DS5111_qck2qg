#!/usr/bin/env python3
import re
from pathlib import Path
import pandas as pd


def normalize_yahoo(csv_path, out_path=None):
    df = pd.read_csv(csv_path)

    # Example: "7.93 +3.40 (75.06%)"
    parts = df["Price"].astype(str)
    df["price"] = parts.str.split().str[0]
    df["change"] = parts.str.split().str[1]
    df["perc_change"] = parts.str.extract(r"\(([-+]?\d+\.?\d*)%")

    out = df.rename(columns={"Symbol": "symbol", "Name": "company_name", "Volume": "volume"})[
        ["symbol", "company_name", "price", "change", "perc_change", "volume"]
    ]

    out_path = Path(out_path or "ygainers_normalized.csv")
    out.to_csv(out_path, index=False)
    return out_path


def normalize_wsj(csv_path, out_path=None):
    df = pd.read_csv(csv_path)

    # --- pick the "company (TICKER)" column ---
    candidates = ["Company", "Name", "Unnamed: 0"]
    comp_col = next((c for c in candidates if c in df.columns), None)
    if comp_col is None:
        # fallback: first column, or any column containing "(TICKER)"
        comp_col = df.columns[0]
        if not df[comp_col].astype(str).str.contains(r"\([A-Z\.]+\)\s*$").any():
            for c in df.columns:
                if df[c].astype(str).str.contains(r"\([A-Z\.]+\)\s*$").any():
                    comp_col = c
                    break

    # --- numeric columns (common WSJ variants) ---
    def pick(names, default=None):
        for n in names:
            if n in df.columns:
                return n
        return default

    price_col = pick(["Price", "Last", "Last Price"])
    chg_col   = pick(["Chg", "Change"])
    pct_col   = pick(["% Chg", "% Change", "Percent Change"])
    vol_col   = pick(["Volume", "Vol", "Vol."])

    if not all([price_col, chg_col, pct_col, vol_col]):
        raise ValueError(f"Couldn't find expected columns. Have: {list(df.columns)}")

    # --- extract symbol + clean company name ---
    rex = r"\(([A-Z\.]+)\)\s*$"
    df["symbol"] = df[comp_col].astype(str).str.extract(rex, expand=False)
    df["company_name"] = df[comp_col].astype(str).str.replace(r"\s*\([A-Z\.]+\)\s*$", "", regex=True).str.strip()
    df = df.dropna(subset=["symbol"]).copy()

    # --- coerce numerics ---
    def to_float(x):
        s = str(x).strip().replace(",", "").replace("$", "").replace("%", "")
        try:
            return float(s)
        except Exception:
            return None

    df["price"] = df[price_col].map(to_float)
    df["change"] = df[chg_col].map(to_float)
    df["perc_change"] = df[pct_col].map(to_float)
    df["volume"] = df[vol_col].astype(str).str.strip().str.upper()

    out = df[["symbol", "company_name", "price", "change", "perc_change", "volume"]]
    out_path = Path(out_path or "wsjgainers_normalized.csv")
    out.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    # Quick manual test (expects ygainers.csv and wsjgainers.csv in CWD)
    print("Normalizing Yahoo ->", normalize_yahoo("ygainers.csv"))
    print("Normalizing WSJ   ->", normalize_wsj("wsjgainers.csv"))

