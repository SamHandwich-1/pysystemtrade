"""
Thin mini-portfolio runner: EWMAC + carry (CSV only, no GUI).

Usage:
    python -m local.first_system.run_system
"""

from sysdata.config.configdata import Config
from sysdata.sim.csv_futures_sim_data import csvFuturesSimData

from systems.accounts.accounts_stage import Account
from systems.basesystem import System
from systems.forecast_combine import ForecastCombine
from systems.forecast_scale_cap import ForecastScaleCap
from systems.forecasting import Rules
from systems.portfolio import Portfolios
from systems.positionsizing import PositionSizing
from systems.rawdata import RawData


def first_system(data=None, config=None):
    if config is None:
        config = Config("local.first_system.config.yaml")
    if data is None:
        data = csvFuturesSimData()

    return System(
        [
            Account(),
            Portfolios(),
            PositionSizing(),
            ForecastCombine(),
            ForecastScaleCap(),
            Rules(),
            RawData(),
        ],
        data,
        config,
    )


def main():
    system = first_system()
    portfolio = system.accounts.portfolio()
    sharpe = float(portfolio.sharpe())
    stats = portfolio.percent.stats()

    print("instruments=", system.get_instrument_list())
    print("sharpe=", round(sharpe, 4))
    print("stats=", stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
