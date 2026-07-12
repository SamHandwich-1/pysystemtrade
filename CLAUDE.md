# pysystemtrade — agent notes

Local working copy of [pst-group/pysystemtrade](https://github.com/pst-group/pysystemtrade) (Rob Carver’s systematic futures engine). Workspace folder is spelled `pysytemtrade` (typo); do not rename mid-work.

## Verified (harness A)

This install is **verified** when all of the following hold on this machine. Re-run after dependency or data changes; do not treat unverified as green.

1. Repo at workspace root with full git history; `origin` → `https://github.com/pst-group/pysystemtrade.git`; branch `develop`.
2. Python 3.10+ venv at `.venv` with editable install `pip install --editable ".[dev]"`.
3. Smoke: `csvFuturesSimData()` loads bundled CSV instruments (252 on first verify).
4. Single-instrument EWMAC intro path produces finite forecasts and account stats (golden below).
5. Fast pytest subset exits 0: `python -m pytest syscore/tests sysdata/tests systems/tests -q --tb=line`.

**Out of scope until a later phase:** IB Gateway/TWS, arctic, full production crontab/Parquet pipelines. Mongo local slice is started (see below). Custom strategies live in `local/first_system/`.

## Remotes

| Remote | URL | Role |
|--------|-----|------|
| `origin` | `https://github.com/pst-group/pysystemtrade.git` | Upstream (fetch / merge) |
| `fork` | `https://github.com/SamHandwich-1/pysystemtrade.git` | Your writable fork (push) |

Push target: `git push fork develop` (no write access to `pst-group`).

## Environment

| Item | Value (first verify) |
|------|----------------------|
| OS | Windows 10/11 |
| Python | 3.11.9 (`py -3.11`) — 3.10 not installed; `requires-python >=3.10` |
| Git HEAD | `883c8681cf880d83acad5c39b842403a8eac5676` (`develop`) |
| Package | pysystemtrade 1.8.2 (editable) |
| pandas / numpy | 2.1.3 / 1.26.4 |

Clone note: full clone failed repeatedly on network resets; used blobless clone (`--filter=blob:none --single-branch --branch develop`) then moved into root. Commit DAG and `origin` are intact; blobs fetch on demand. Prefer `git fetch` / merge against `origin` rather than re-downloading.

## Commands

```powershell
cd C:\Users\james\Projects\pysytemtrade
.\.venv\Scripts\Activate.ps1

# Smoke
python -c "from sysdata.sim.csv_futures_sim_data import csvFuturesSimData; d=csvFuturesSimData(); print(d); print(len(d.get_instrument_list()))"

# Fast tests
python -m pytest syscore/tests sysdata/tests systems/tests -q --tb=line

# Phase B mini-portfolio
python -m local.first_system.run_system

# Reinstall (after dep changes)
python -m pip install --editable ".[dev]"
```

There is no top-level `import pysystemtrade`; packages are `sysdata`, `systems`, `syscore`, etc.

## Golden EWMAC baseline (this machine)

Canonical script: [`examples/introduction/asimpletradingrule.py`](examples/introduction/asimpletradingrule.py) (non-interactive: skip `matplotlib` `show()`).

| Field | Value |
|-------|--------|
| Instrument | `VIX` |
| Rule | EWMAC Lfast=32, Lslow=128 via `robust_vol_calc` |
| Forecast finite | yes |
| Forecast tail (last 5) | 2024-03-21…27 ≈ -6.915, -6.889, -6.872, -6.875, -6.897 |
| Sharpe (`account.percent.sharpe()`) | **0.4992** |
| Other stats (rounded) | ann_mean 5.222, ann_std 10.46, hitrate 0.5378 |

Regression rule: re-run the same recipe; Sharpe should stay within ~0.01 of **0.4992** and forecast tails should not silently flip sign or go non-finite unless CSV data or code changed (then update this section with new HEAD + versions).

### Carver published numbers (best-effort)

Older intro docs published May 2016 EWMAC(32,128) tails ≈ 4.60…5.08 and Sharpe ≈ 0.5084 (instrument then EDOLLAR / later SOFR). Bundled data has moved on:

- `EDOLLAR` is not in the current instrument list (use `SOFR`).
- `SOFR` on those dates: ≈ 4.42…4.86 (max abs diff vs published ≈ 0.22) — same shape/sign, not an exact match.
- Docs themselves warn results differ with refreshed CSV data.

So “matches Carver” for this harness means: **same pipeline as the intro example** + **match the pinned local golden** (above). Exact equality to blog/doc numerics is not required and is not expected after data refresh.

## Phase B golden — `local/first_system`

CSV-only portfolio (no Mongo/IB): widened instruments, multi-speed EWMAC + carry, scale and weight estimates.

| Field | Value |
|-------|--------|
| Runner | `python -m local.first_system.run_system` |
| Config | [`local/first_system/config.yaml`](local/first_system/config.yaml) |
| Instruments | `SOFR`, `US10`, `EUROSTX`, `MXP`, `CORN`, `V2X` |
| Active rules | all six EWMACs (`2_8` … `64_256`) + `carry` |
| Estimates | forecast scale (pooled), forecast weights/FDM (`one_period`), instrument weights/IDM (`shrinkage` / `in_sample`) |
| Capital / vol | USD 250000, 20% vol target |
| Portfolio Sharpe | **0.4229** |
| Other stats (rounded) | ann_mean 9.074, ann_std 21.46, hitrate 0.4971 |
| Prior goldens | … → 0.4905 → 0.5690 (without fastest two EWMACs) |

Regression rule: re-run the runner; portfolio Sharpe within ~0.01 of **0.4229** unless CSV data or `local/first_system` config/code changed (then update this section).

## Layout pointers

- Backtest intro: `docs/introduction.md`, `docs/backtesting.md`
- Install: `docs/installation.md`
- Data: `sysdata/`; sim CSV via `csvFuturesSimData`
- Provided systems: `systems/provided/`
- Local custom systems: `local/` (committed; do not use gitignored `private/` for golden baselines)
