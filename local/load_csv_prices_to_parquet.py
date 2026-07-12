"""
Load shipped CSV multiple + adjusted prices into the local Parquet store
for the first_system instrument set (no interactive prompt).

Usage:
    python -m local.load_csv_prices_to_parquet
"""

from sysinit.futures.multiple_and_adjusted_from_csv_to_db import (
    init_db_with_csv_prices_for_code,
)
from sysproduction.data.prices import diagPrices

INSTRUMENTS = ["SOFR", "US10", "EUROSTX", "MXP", "CORN", "V2X"]


def main():
    for instrument_code in INSTRUMENTS:
        init_db_with_csv_prices_for_code(instrument_code)

    prices = diagPrices()
    adj_ok = []
    mult_ok = []
    for instrument_code in INSTRUMENTS:
        adj = prices.get_adjusted_prices(instrument_code)
        mult = prices.get_multiple_prices(instrument_code)
        adj_len = 0 if adj is None else len(adj.dropna())
        mult_len = 0 if mult is None else len(mult.dropna())
        print(f"{instrument_code}: adjusted_rows={adj_len} multiple_rows={mult_len}")
        if adj_len > 0:
            adj_ok.append(instrument_code)
        if mult_len > 0:
            mult_ok.append(instrument_code)

    if set(adj_ok) != set(INSTRUMENTS) or set(mult_ok) != set(INSTRUMENTS):
        missing = set(INSTRUMENTS) - (set(adj_ok) & set(mult_ok))
        print("FAIL: missing parquet prices for", missing)
        return 1

    print("csv_to_parquet_verified instruments=", len(INSTRUMENTS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
