# RealT DEX Price Premium Analysis

## What this is

Real-world-asset (RWA) tokens are supposed to track the value of the asset behind them — but do they? This repo is the data-collection half of a research project investigating whether RealT's tokenized US real-estate tokens ("house tokens", mostly Detroit single-family homes) trade at a premium or discount to their appraised net asset value on decentralised exchanges, and what drives that gap. The pipeline reconstructs every on-chain swap of RealT house tokens — 46k trades on Levinswap (Gnosis Chain) and 5.5k pre-2021 trades on Uniswap V1 (Ethereum) — then enriches each trade with the property's offering price, city-level house-price-index growth since offering, holder count, trading volume, transaction fees, and the total crypto market cap at the time of the trade. The result is a per-trade panel dataset (`final.csv`, ~51,900 rows across 263 properties) where each row carries both the token's implied on-chain market cap and an index-adjusted off-chain valuation of the underlying house, so the premium can be measured directly. The statistical modelling itself was done downstream and is not in this repo.

## How the premium is measured

For each swap:

- **On-chain side:** the swap's exchange rate gives a USD token price; multiplied by token supply this gives `on_chain_market_cap`.
- **Off-chain side:** the property's initial market cap (net of RealT's issuance premium) is grown forward by the change in its city's house-price index between the offering date and the trade date, giving `valuation_t` (`growth_rate = index_at_trade / index_at_offering`).
- **`price_premium`** is the difference between the two — how much the market values the token above or below the index-adjusted value of the house.

## Data sources

Everything below is what the code actually calls or reads.

| Source | Used for |
|---|---|
| GnosisScan API (`api.gnosisscan.io`) | Raw transaction lists for the Levinswap router, contract ABIs, factory event logs to enumerate house-token contract addresses |
| Blockscout API v2 (`gnosis.blockscout.com`, `eth.blockscout.com`) | Token symbols, names, supplies, holder counts; per-transaction transfer volumes and fees on both chains |
| Etherscan API (`api.etherscan.io`) | Gas price and value for the pre-2021 Uniswap V1 transactions on Ethereum |
| Gnosis/Ethereum RPC nodes (QuikNode, Infura) via web3.py / web3.js | Decoding swap calldata against the router ABI, reading transaction receipts and event logs |
| `realt.co` product pages (requests + BeautifulSoup) | Offering date and token contract address for each property |
| RealT community "YAM" spreadsheet (CSV export, `yamInfoNew.csv`) | Per-property city, RealT list price, APR, RMM flag, supply and traded volume |
| City house-price indices (`Monthly Data.csv`, `Quarterly Data.csv`) | Index levels for Detroit, Cleveland, Chicago, Miami (monthly) and Birmingham, Toledo, Kissimmee, Rochester, Akron, Jackson (quarterly) |
| `Crypto_Total_Market_Cap.csv` | Total crypto market cap, as-of merged onto each trade as a market-sentiment control |
| `uniswap_pre_2021.xlsx` | Per-property sheets of early Uniswap V1 trades (11 properties) for the Ethereum leg |

## Pipeline

### Round 1 — `First_Analysis_Round/`: build the Gnosis Chain trade panel

| Script | What it does |
|---|---|
| `DEX_PRICES.py` | Walks Gnosis blocks ~14.06M–32M, pulls every transaction sent to the Levinswap router, decodes the six Uniswap-V2-style `swap*` calldata variants, and writes one row per swap with the implied exchange rate → `transaction_data.csv` (~90k swaps) |
| `get_first_batch_houses.py`, `get_second_batch_houses.py`, `second_batch.js` | Enumerate RealT house-token contract addresses from the RealT deployer's contract-creation transactions and the token factory's event logs |
| `refineTokens.py` (supersedes `filter_transactionsOLD.py`) | Filters the swap list down to trades involving a house token → `filtered_transactions.csv` (~50k trades) |
| `add_data.py`, `add_data_2.py`, `add_data3.py` | Enrich each trade with token symbol, total supply, and token name from Blockscout; derive a normalised `name_short` (with a hand-maintained exception map for inconsistent street names) |
| `yamInfo.py`, `editingyaminfoname.py` | Normalise token symbols and YAM spreadsheet names to a common join key |
| `merging.py` | Joins trades to the YAM property data (city, RealT price, APR, RMM flag, volume) → `merged_dataset.csv` |
| `add_holdercount.py` | Adds per-token holder counts from Blockscout → `merged_dataset_2.csv` |
| `format_into_numbers.py` | Strips `$`/formatting from price columns → `merged_dataset_3.csv` |
| `get_offering_date`, `merging_times.py` | Scrapes each property's offering date and token address from realt.co, converts to timestamps, merges in → `merged_dataset_4.csv` |
| `gen_projections.py` | Maps each property's city to its house-price index, computes index growth from offering date to trade date, and produces the index-adjusted valuation `valuation_t` → `merged_dataset_5.csv` |

### Round 2 — root + `Second_Analysis_Round/`: fees, volumes, controls, and the Ethereum leg

Gnosis leg (continues from the Round 1 output, carried forward as `April_*.csv`):

| Script | What it does |
|---|---|
| `Second_Analysis_Round/add_crypto_market.py` | As-of merges total crypto market cap onto each trade by timestamp |
| `big_api.py`, `Second_Analysis_Round/add_fees_and_value.py`, `filling_out_data.py`, `merge_aprils.py` | Fetch per-transaction token-transfer volumes, native value, and fees from Gnosis Blockscout (threaded, with retries), and backfill rows the first pass missed |
| `cleanup.py` | Parses Blockscout's `{value, decimals}` volume payloads into plain decimal amounts |
| `Second_Analysis_Round/add_value.py` | Computes each trade's USD `transaction_value` from whichever side of the swap is the quote stablecoin (token `0xe91D…a97d`) → `April_5.csv` |

Ethereum leg (pre-2021 Uniswap V1 trades):

| Script | What it does |
|---|---|
| `merge uniswap.py`, `gen_housetoken.py` | Merge the 11 per-property sheets of `uniswap_pre_2021.xlsx` into one table and derive the house-token symbol per trade |
| `Second_Analysis_Round/add_volumes,py` | Derives volume/token bought and sold from the raw In/Out swap columns → `uniswap_3.csv` |
| `scrape_value_fees.py` | Pulls gas price and transaction value per trade from Etherscan |
| `Second_Analysis_Round/add_crypto_market.py`, `tx_fees.py` | Add the crypto-market-cap control and the ETH transaction fee (from `eth.blockscout.com`) → `uniswap_8.csv` |

Final assembly:

| Script | What it does |
|---|---|
| `concat_data.py` | Concatenates the Gnosis panel (`April_5.csv`) and the Ethereum panel (`uniswap_8.csv`) on their shared columns → `final.csv` |

## Output datasets

**`final.csv`** — the main deliverable. One row per DEX swap of a RealT house token: 51,857 trades (46,304 Levinswap / 5,553 Uniswap V1) across 263 properties. Key columns:

- Trade: `tx_hash`, `timestamp`, `token_sold` / `token_bought`, `volume_sold` / `volume_bought`, `token_price` (USD), `transaction_fee_usd`, `DEX`
- Token/property: `house_token` (contract address), `token_name`, `token_symbol`, `token_supply`, `city`, `realt_price_original`, `realt_apr`, `rmm` (whether the token is usable as RMM lending collateral), `holders_count`, `volume_total`, `offering_date_timestamp`
- Valuation: `on_chain_market_cap`, `initial_market_cap`, `initial_market_cap_without_premium`, `initial_index_value`, `transaction_index_value`, `growth_rate`, and the target variable `price_premium`

**`final_2.csv`** — same 51,857 trades and schema minus the three raw index columns (`initial_index_value`, `transaction_index_value`, `growth_rate`).

**`First_Analysis_Round/merged_dataset_5.csv`** — the end of the Round 1 pipeline: the 50,168 Gnosis trades with property data, holder counts, offering dates, and the index-adjusted `valuation_t`, before the Round 2 fee/volume enrichment.

Intermediate files (`transaction_data.csv`, `sorted_transactions_*.csv`, `merged_dataset_*.csv`, `uniswap_*.csv`, `April_*.csv`) are kept so each stage is inspectable.

## Caveats

- **This is the data-construction half.** The econometric analysis of what drives the premium was done downstream and is not in this repo.
- **API keys are required** for GnosisScan, Etherscan, and an RPC provider; keys in the committed scripts are censored or placeholders.
- **Some steps were manual.** A few intermediate files (e.g. the `sorted_transactions` price step, `uniswap_4`–`uniswap_6`, and the Round 2 starting file `April_2.csv`) were produced by hand or in a spreadsheet between scripted stages, and one referenced input (`Crypto_Total_Market_Cap.csv`) is not committed. Name normalisation between on-chain token symbols and the YAM spreadsheet also needed a hand-maintained exception list.
- **Column-name drift.** The two legs name a few columns differently (e.g. `crypto_total_market_cap` vs `total_crypto_market_cap`, and a `transcation_value_usd` typo), so `concat_data.py` — which keeps only exactly-matching columns — drops those from `final.csv`; they survive in the per-leg files.
- Scripts are one-shot research code: file paths are hard-coded and stages are run in order by hand, not orchestrated.
