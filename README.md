# Binance Futures Testnet API Client

A small Python command-line application for submitting MARKET and LIMIT orders to the Binance USDⓈ-M Futures **Testnet**. It demonstrates signed REST requests, input validation, modular code organization, logging, and error handling.

> **Safety:** This client is restricted to `https://testnet.binancefuture.com`. It is for educational testing, not production trading or financial advice. Testnet use can still have consequences within your test account.

## Features

- HMAC-SHA256 signatures for authenticated requests
- MARKET and LIMIT orders with BUY and SELL sides
- CLI input validation, including rejection of non-finite quantities/prices
- Request timeout and handling for network and HTTP errors
- Rotating log files and concise console warnings
- Unit tests for validation, request signing, and mocked HTTP responses

## Project structure

```text
binance-futures-api-client/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
├── tests/
│   ├── test_client.py
│   └── test_validators.py
├── .env.example
├── .gitignore
├── cli.py
├── README.md
└── requirements.txt
```

## Requirements

- Python 3.10 or newer
- Binance Futures Testnet API credentials

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Set testnet credentials

Create API credentials from the Binance Futures Testnet environment. Set the environment variables in your shell.

Windows PowerShell:

```powershell
$env:BINANCE_TESTNET_API_KEY="your_testnet_api_key"
$env:BINANCE_TESTNET_API_SECRET="your_testnet_api_secret"
```

macOS/Linux:

```bash
export BINANCE_TESTNET_API_KEY="your_testnet_api_key"
export BINANCE_TESTNET_API_SECRET="your_testnet_api_secret"
```

`.env.example` is a reference template; this project does not automatically load `.env` files. Do not commit real credentials.

## Usage

Show available arguments:

```bash
python cli.py --help
```

Example MARKET order:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Example LIMIT order:

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

These examples send order requests when valid testnet credentials are configured. Do not run them unless you intend to submit test orders.

## Run tests

The tests use Python's standard `unittest` framework and mock HTTP requests; they do not send real orders.

```bash
python -m unittest discover -s tests -v
```

## Design notes

- `client.py` handles request signing, HTTP communication, and API errors.
- `validators.py` validates user input before client initialization and API calls.
- `orders.py` keeps order orchestration and response formatting separate from the CLI.
- `logging_config.py` configures rotating file logging.
- `cli.py` handles command-line arguments and user-facing errors.

The symbol validator checks format, not whether a symbol is currently tradable. Binance remains responsible for validating exchange-specific rules such as lot size, tick size, and account permissions.

## Limitations

This is a learning project, not a production trading system. It does not implement retries, exchange metadata/step-size validation, order cancellation, position management, or a comprehensive integration test suite. Successful local tests do not guarantee that an order will be accepted by the exchange.

## License

No license has been selected. Add a license file before allowing others to reuse or redistribute this project.
