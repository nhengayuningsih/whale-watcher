import requests
import time
from datetime import datetime

THRESHOLD_USD = 1_000_000
CHECK_INTERVAL = 60
WHALE_ALERT_API = "https://api.whale-alert.io/v1/transactions"
API_KEY = "demo"  # Замени на свой API-ключ с https://www.whale-alert.io/

def fetch_whale_transactions():
    params = {
        "api_key": API_KEY,
        "min_value": THRESHOLD_USD,
        "start": int(time.time()) - CHECK_INTERVAL,
        "limit": 10,
        "currency": "usd"
    }
    response = requests.get(WHALE_ALERT_API, params=params)
    if response.status_code != 200:
        print("Ошибка запроса:", response.status_code)
        return []
    return response.json().get("transactions", [])

def notify(transaction):
    amount = transaction["amount"]
    symbol = transaction["symbol"]
    from_addr = transaction["from"]["address"]
    to_addr = transaction["to"]["address"]
    value_usd = transaction["amount_usd"]
    timestamp = datetime.fromtimestamp(transaction["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')

    print(f"""
🕵️ Whale Alert:
{amount} {symbol} (${value_usd:,.0f}) transferred
From: {from_addr}
To: {to_addr}
Time: {timestamp}
    """)

def main():
    print("🔍 Whale Watcher активен...")
    while True:
        try:
            transactions = fetch_whale_transactions()
            for tx in transactions:
                notify(tx)
        except Exception as e:
            print("Ошибка:", e)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
