import unittest
from unittest.mock import Mock, patch
import requests
from urllib.parse import urlencode
import hashlib
import hmac

from bot.client import BinanceAPIError, BinanceFuturesTestnetClient


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = BinanceFuturesTestnetClient("test-key", "test-secret")

    def test_rejects_non_testnet_base_url(self):
        with self.assertRaises(ValueError):
            BinanceFuturesTestnetClient("key", "secret", base_url="https://fapi.binance.com")

    @patch("bot.client.time.time", return_value=123.0)
    def test_signature_matches_query_string(self, _):
        result = self.client._sign({"symbol": "BTCUSDT", "side": "BUY"})
        unsigned = {k: v for k, v in result.items() if k != "signature"}
        expected = hmac.new(
            b"test-secret", urlencode(unsigned).encode(), hashlib.sha256
        ).hexdigest()
        self.assertEqual(result["signature"], expected)
        self.assertEqual(result["timestamp"], 123000)

    @patch.object(requests.Session, "request")
    def test_successful_order_response(self, request_mock):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"orderId": 123, "status": "NEW"}
        request_mock.return_value = response

        result = self.client.place_order("BTCUSDT", "BUY", "MARKET", 0.01)
        self.assertEqual(result["orderId"], 123)
        request_mock.assert_called_once()

    @patch.object(requests.Session, "request")
    def test_http_error_raises_api_error(self, request_mock):
        response = Mock()
        response.status_code = 400
        response.json.return_value = {"code": -1, "msg": "invalid request"}
        request_mock.return_value = response

        with self.assertRaises(BinanceAPIError):
            self.client.place_order("BTCUSDT", "BUY", "MARKET", 0.01)


if __name__ == "__main__":
    unittest.main()
