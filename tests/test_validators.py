import math
import unittest

from bot.validators import (
    ValidationError, validate_order_type, validate_price,
    validate_quantity, validate_side, validate_symbol,
)


class ValidatorTests(unittest.TestCase):
    def test_symbol_is_normalized(self):
        self.assertEqual(validate_symbol(" btcusdt "), "BTCUSDT")

    def test_invalid_symbol_rejected(self):
        with self.assertRaises(ValidationError):
            validate_symbol("BTC-USDT")

    def test_side_and_type_are_normalized(self):
        self.assertEqual(validate_side(" buy "), "BUY")
        self.assertEqual(validate_order_type("market"), "MARKET")

    def test_invalid_side_rejected(self):
        with self.assertRaises(ValidationError):
            validate_side("HOLD")

    def test_quantity_must_be_positive_finite(self):
        for value in (0, -1, "NaN", "Infinity", "-Infinity", "abc"):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validate_quantity(value)

    def test_limit_price_required_and_positive_finite(self):
        for value in (None, 0, -2, "NaN", "Infinity", "bad"):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    validate_price(value, "LIMIT")

    def test_market_price_is_ignored(self):
        self.assertIsNone(validate_price(None, "MARKET"))
        self.assertIsNone(validate_price("not-used", "MARKET"))


if __name__ == "__main__":
    unittest.main()
