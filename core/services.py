import requests
from django.core.cache import cache

CACHE_KEY = "coingecko_crypto_data"
CACHE_TIME = 300  


def get_crypto_data():
    cached = cache.get(CACHE_KEY)
    if cached:
        return cached

    data = {
        "btc": 0,
        "eth": 0,
        "usdt": 1,
        "btc_volume": 0,
        "active_trades": 0,
    }

    try:
        prices = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": "bitcoin,ethereum,tether",
                "vs_currencies": "usd",
                "include_24hr_vol": "true",
            },
            timeout=10,
        )
        prices.raise_for_status()
        prices = prices.json()

        global_data = requests.get(
            "https://api.coingecko.com/api/v3/global",
            timeout=10,
        )
        global_data.raise_for_status()
        global_data = global_data.json()

        data = {
            "btc": prices.get("bitcoin", {}).get("usd", 0),
            "eth": prices.get("ethereum", {}).get("usd", 0),
            "usdt": prices.get("tether", {}).get("usd", 1),
            "btc_volume": prices.get("bitcoin", {}).get("usd_24h_vol", 0),
            "active_trades": global_data.get("data", {}).get(
                "active_cryptocurrencies", 0
            ),
        }
        cache.set(CACHE_KEY, data, CACHE_TIME)

    except requests.RequestException as e:
        print("CoinGecko Error:", e)

        old = cache.get(CACHE_KEY)
        if old:
            return old

    return data