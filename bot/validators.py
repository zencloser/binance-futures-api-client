"""Input validation for command-line order parameters."""

import math
import re

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,20}$")


class ValidationError(ValueError):
    """Raised when user-supplied input fails validation."""


def validate_symbol(symbol: str) -> str:
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValidationError("Symbol is required")
    symbol = symbol.strip().upper()
    if not SYMBOL_PATTERN.fullmatch(symbol):
        raise ValidationError(
            f"Invalid symbol format: {symbol!r}. Example: BTCUSDT"
        )
    return symbol


def validate_side(side: str) -> str:
    if not isinstance(side, str):
        raise ValidationError("Side must be BUY or SELL")
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side: {side!r}. Choose BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    if not isinstance(order_type, str):
        raise ValidationError("Order type must be MARKET or LIMIT")
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type: {order_type!r}. Choose MARKET or LIMIT"
        )
    return order_type


def _positive_finite_number(value, field_name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValidationError(f"{field_name} must be a number, got: {value!r}") from exc
    if not math.isfinite(number):
        raise ValidationError(f"{field_name} must be a finite number")
    if number <= 0:
        raise ValidationError(f"{field_name} must be greater than 0")
    return number


def validate_quantity(quantity) -> float:
    return _positive_finite_number(quantity, "Quantity")


def validate_price(price, order_type: str):
    """Require a positive finite price for LIMIT orders; ignore it for MARKET."""
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
        return _positive_finite_number(price, "Price")
    return None
