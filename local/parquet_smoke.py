"""
Parquet smoke: resolve parquet_store from private config, write/read a probe frame.

Usage:
    python -m local.parquet_smoke
"""

import pandas as pd

from sysdata.config.production_config import get_production_config
from sysdata.parquet.parquet_access import ParquetAccess


def main():
    config = get_production_config()
    store = config.get_element("parquet_store")
    print("parquet_store=", store)

    access = ParquetAccess(store)
    probe = pd.DataFrame(
        {"value": [1.0, 2.0, 3.0]},
        index=pd.date_range("2020-01-01", periods=3, freq="B"),
    )
    data_type = "harness_smoke"
    identifier = "parquet_smoke"

    access.write_data_given_data_type_and_identifier(
        data_to_write=probe, data_type=data_type, identifier=identifier
    )
    got = access.read_data_given_data_type_and_identifier(
        data_type=data_type, identifier=identifier
    )

    if got is None or len(got) != 3 or float(got["value"].iloc[-1]) != 3.0:
        print("FAIL: probe parquet missing or invalid:", got)
        return 1

    exists = access.does_identifier_with_data_type_exist(
        data_type=data_type, identifier=identifier
    )
    print("probe_rows=", len(got), "exists=", exists)
    print("parquet_verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
