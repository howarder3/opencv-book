import requests

TELEGRAM_TOKEN = "你的Token"
TELEGRAM_CHAT_ID = "你的ChatID"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
payload = {"chat_id": TELEGRAM_CHAT_ID, "text": "測試訊息：Telegram Bot 串接成功！"}
response = requests.post(url, json=payload)

if response.ok:
    print("發送成功！請檢查手機上的 Telegram")
else:
    print(f"發送失敗：{response.text}")
