"""
Run first_system against Parquet/Mongo dbFuturesSimData (no GUI).

Prereqs:
    docker start pysystemtrade-mongo
    python -m local.load_csv_prices_to_parquet
    python -m local.seed_db_sim_static

Usage:
    python -m local.first_system.run_system_db
"""

from sysdata.config.configdata import Config
from sysdata.sim.db_futures_sim_data import dbFuturesSimData

from local.first_system.run_system import first_system


def main():
    data = dbFuturesSimData()
    print(data)
    system = first_system(data=data, config=Config("local.first_system.config.yaml"))
    portfolio = system.accounts.portfolio()
    sharpe = float(portfolio.sharpe())
    stats = portfolio.percent.stats()

    print("data_source=dbFuturesSimData")
    print("instruments=", system.get_instrument_list())
    print("sharpe=", round(sharpe, 4))
    print("stats=", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
