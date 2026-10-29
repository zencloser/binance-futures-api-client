"""Order orchestration and human-readable response formatting."""

import logging

from bot.client import BinanceFuturesTestnetClient

logger = logging.getLogger("trading_bot")


def build_order_summary(
    symbol: str, side: str, order_type: str, quantity: float, price: float = None
) -> str:
    lines = [
        "Order Request Summary",
        "----------------------",
        f"Symbol   : {symbol}",
        f"Side     : {side}",
        f"Type     : {order_type}",
        f"Quantity : {quantity}",
    ]
    if order_type == "LIMIT":
        lines.append(f"Price    : {price}")
    return "\n".join(lines)


def place_order(
    client: BinanceFuturesTestnetClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
) -> dict:
    logger.info(
        "Placing order: symbol=%s side=%s type=%s qty=%s price=%s",
        symbol, side, order_type, quantity, price,
    )
    return client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )


def format_order_response(response: dict) -> str:
    fields = (
        ("Order ID", "orderId"),
        ("Status", "status"),
        ("Executed Qty", "executedQty"),
        ("Avg Price", "avgPrice"),
    )
    lines = ["Order Response", "---------------"]
    lines.extend(f"{label:<13}: {response.get(key, 'N/A')}" for label, key in fields)
    return "\n".join(lines)
