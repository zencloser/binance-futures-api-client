"""CLI for placing MARKET or LIMIT orders on Binance Futures Testnet."""

import argparse
import os
import sys

from bot.client import BinanceAPIError, BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import build_order_summary, format_order_response, place_order
from bot.validators import (
    ValidationError,
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Place an order on Binance USDⓈ-M Futures Testnet."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Positive order quantity")
    parser.add_argument("--price", help="Required for LIMIT orders")
    return parser.parse_args()


def main() -> int:
    logger = setup_logging()
    args = parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except ValidationError as exc:
        logger.warning("Input validation failed: %s", exc)
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    print(build_order_summary(symbol, side, order_type, quantity, price))
    print()

    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")
    try:
        client = BinanceFuturesTestnetClient(api_key=api_key, api_secret=api_secret)
    except ValueError as exc:
        logger.warning("Client configuration failed: %s", exc)
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    try:
        response = place_order(client, symbol, side, order_type, quantity, price)
    except (ConnectionError, BinanceAPIError) as exc:
        logger.warning("Order request failed: %s", exc)
        print(f"Order failed: {exc}", file=sys.stderr)
        return 1
    except Exception:
        logger.exception("Unexpected error while placing order")
        print("Unexpected error. Check logs/trading_bot.log for details.", file=sys.stderr)
        return 1

    print(format_order_response(response))
    print("\nSUCCESS: Testnet API accepted the order request.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
