"""
Seed FX (Parquet) and spread costs (Mongo) from shipped CSV for dbFuturesSimData.

Usage:
    python -m local.seed_db_sim_static
"""

from sysdata.csv.csv_spot_fx import csvFxPricesData
from sysdata.csv.csv_spread_costs import csvSpreadCostData
from sysdata.mongodb.mongo_spread_costs import mongoSpreadCostData
from sysproduction.data.currency_data import dataCurrency


def seed_fx():
    csv_fx = csvFxPricesData()
    db_fx = dataCurrency().db_fx_prices_data
    codes = csv_fx.get_list_of_fxcodes()
    for code in codes:
        fx_prices = csv_fx.get_fx_prices(code)
        db_fx.add_fx_prices(code=code, fx_price_data=fx_prices, ignore_duplication=True)
        print(f"fx {code}: rows={len(fx_prices)}")
    return codes


def seed_spread_costs():
    csv_costs = csvSpreadCostData()
    mongo_costs = mongoSpreadCostData()
    instruments = csv_costs.get_list_of_instruments()
    for instrument_code in instruments:
        cost = csv_costs.get_spread_cost(instrument_code)
        mongo_costs.update_spread_cost(instrument_code, cost)
    print(f"spread_costs: instruments={len(instruments)}")
    return instruments


def main():
    fx_codes = seed_fx()
    cost_instruments = seed_spread_costs()
    if not fx_codes or not cost_instruments:
        print("FAIL: empty FX or spread cost seed")
        return 1
    print("db_sim_static_verified fx=", len(fx_codes), "costs=", len(cost_instruments))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
