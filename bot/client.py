"""Minimal signed REST client for Binance USDⓈ-M Futures Testnet."""

import hashlib
import hmac
import logging
import math
import time
from urllib.parse import urlencode, urlparse

import requests

logger = logging.getLogger("trading_bot")


class BinanceAPIError(RuntimeError):
    """Raised when Binance returns a non-success HTTP response."""


class BinanceFuturesTestnetClient:
    """Small REST client deliberately restricted to the Binance Futures Testnet."""

    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = BASE_URL,
        timeout: float = 10,
    ):
        if not api_key or not api_secret:
            raise ValueError(
                "API key and secret are required. Set "
                "BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET."
            )
        parsed = urlparse(base_url)
        if parsed.scheme != "https" or parsed.hostname != "testnet.binancefuture.com":
            raise ValueError("Only https://testnet.binancefuture.com is allowed")
        if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be a positive finite number")

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> dict:
        signed_params = dict(params)
        signed_params["timestamp"] = int(time.time() * 1000)
        signed_params["recvWindow"] = 5000
        query_string = urlencode(signed_params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed_params["signature"] = signature
        return signed_params

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        signed: bool = False,
    ) -> dict:
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("API path must be a relative absolute-path such as /fapi/v1/order")

        request_params = dict(params or {})
        if signed:
            request_params = self._sign(request_params)

        # Never log the API secret, API-key header, or request signature.
        loggable_params = {
            key: value for key, value in request_params.items()
            if key not in {"signature"}
        }
        url = f"{self.base_url}{path}"
        logger.info("REQUEST %s %s | params=%s", method.upper(), url, loggable_params)

        try:
            response = self.session.request(
                method.upper(), url, params=request_params, timeout=self.timeout
            )
        except requests.exceptions.RequestException as exc:
            logger.warning("Network error on %s %s: %s", method.upper(), path, exc)
            raise ConnectionError("Network error while calling Binance Testnet API") from exc

        try:
            data = response.json()
        except ValueError:
            data = {"raw_response": response.text[:1000]}

        if not 200 <= response.status_code < 300:
            logger.warning(
                "API error %s %s | status=%s | response=%s",
                method.upper(), path, response.status_code, data,
            )
            raise BinanceAPIError(
                f"Binance Testnet API returned HTTP {response.status_code}: {data}"
            )

        logger.info(
            "RESPONSE %s %s | status=%s | response=%s",
            method.upper(), path, response.status_code, data,
        )
        if not isinstance(data, dict):
            raise BinanceAPIError("Unexpected API response: expected a JSON object")
        return data

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
        time_in_force: str = "GTC",
    ) -> dict:
        """Place a MARKET or LIMIT order through POST /fapi/v1/order."""
        if order_type not in {"MARKET", "LIMIT"}:
            raise ValueError("order_type must be MARKET or LIMIT")
        if order_type == "LIMIT" and (price is None or time_in_force not in {"GTC", "IOC", "FOK"}):
            raise ValueError("LIMIT orders require a price and valid time_in_force")

        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force

        return self._request("POST", "/fapi/v1/order", params=params, signed=True)
