#!/usr/bin/env python3
"""Normalize gainer data from WSJ/Yahoo sources."""

from pathlib import Path
import pandas as pd


def normalize_yahoo(csv_path: str | Path, out_path: str | Path | None = None) -> Path:
    """Normalize a Yahoo Finance gainers CSV to a standard schema.

    Returns the output path.
    """
    df = pd.read_csv(csv_path)

    # Example "Price" cell: "7.93 +3.40 (75.06%)"
    parts = df["Price"].astype(str).str.split()

    df["price"] = parts.str[0]
    df["change"] = parts.str[1]
    df["perc_change"] = df["Price"].astype(str).str.extract(r"\(([-+]?\d+(?:\.\d+)?)%")

    out = df.rename(
        columns={"Symbol": "symbol", "Name": "company_name", "Volume": "volume"}
    )[["symbol", "company_name", "price", "change", "perc_change", "volume"]]

    out_path = Path(out_path or "ygainers_normalized.csv")
    out.to_csv(out_path, index=False)
    return out_path


def normalize_wsj(csv_path: str | Path, out_path: str | Path | None = None) -> Path:
    """Normalize a WSJ gainers CSV to a standard schema.

    Returns the output path.
    """
    df = pd.read_csv(csv_path)

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
    def pick(names: list[str], default: str | None = None) -> str | None:
        for n in names:
            if n in df.columns:
                return n
        return default

    price_col = pick(["Price", "Last", "Last Price"])
    chg_col = pick(["Chg", "Change", "Change Net"])
    pct_col = pick(["% Chg", "Change %", "Chg %"])
    vol_col = pick(["Volume", "Vol", "Vol."])

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
    out_path = Path(out_path or "wsjgainers_normalized.csv")
    out.to_csv(out_path, index=False)
    return out_path


if __name__ == "__main__":
    # Quick manual test (expects ygainers.csv and wsjgainers.csv in CWD)
    print("Normalizing Yahoo ->", normalize_yahoo("ygainers.csv"))
    print("Normalizing WSJ   ->", normalize_wsj("wsjgainers.csv"))
