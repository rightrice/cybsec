import requests
import time

# ====== CONFIGURATION ======
UNIFI_API_TOKEN = "your_unifi_api_token"          # UniFi API Token
UNIFI_SITE_ID = "default"                         # Replace if using another site
POLL_INTERVAL = 60                                # Time between checks (in seconds)

TELEGRAM_API_TOKEN = "your_telegram_api_token"    # Telegram Bot Token
TELEGRAM_CHAT_ID = "your_telegram_chat_id"        # Telegram Chat ID

# ====== SPECIFIC AP MAC ADDRESSES TO MONITOR ======
# Get AP MAC addresses via UniFi API or Controller
# You can find your MAC addresses in your UniFi console
WATCHED_APS = {
    "74:ac:b9:12:34:56": "Main Office AP",
    "74:ac:b9:65:43:21": "Lobby AP",
    "74:ac:b9:11:22:33": "Warehouse AP"
}

# ====== HEADERS FOR UNIFI API ======
HEADERS = {
    "Authorization": f"Bearer {UNIFI_API_TOKEN}",
    "Content-Type": "application/json"
}

# ====== UniFi API Base URL ======
UNIFI_BASE_URL = "https://unifi.ui.com/api/s"

# ====== TRACK AP STATUS TO AVOID DUPLICATE ALERTS ======
ap_status_cache = {}

# ====== Send Telegram Message ======
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"[+] Telegram alert sent: {message}")
    else:
        print(f"[-] Failed to send Telegram alert: {response.text}")

# ====== Get List of Access Points ======
def get_access_points():
    url = f"{UNIFI_BASE_URL}/{UNIFI_SITE_ID}/stat/device"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"[-] Failed to fetch AP data: {response.text}")
        return []

# ====== Main Monitoring Loop ======
def main():
    print("[*] Starting UniFi AP Monitoring Bot...")

    while True:
        ap_list = get_access_points()

        # Check each AP in WATCHED_APS
        for ap in ap_list:
            ap_mac = ap.get("mac")
            ap_name = ap.get("name", "Unknown AP")
            ap_state = ap.get("state", 0)  # 1 = Online, 0 = Offline

            if ap_mac in WATCHED_APS:
                readable_name = WATCHED_APS[ap_mac]
                last_status = ap_status_cache.get(ap_mac)

                if ap_state == 1 and last_status != "online":
                    # AP is now online
                    msg = f"✅ *{readable_name}* is now *ONLINE* 🟢"
                    send_telegram_message(msg)
                    ap_status_cache[ap_mac] = "online"

                elif ap_state == 0 and last_status != "offline":
                    # AP went offline
                    msg = f"⚠️ *ALERT*: *{readable_name}* is *OFFLINE* 🔴"
                    send_telegram_message(msg)
                    ap_status_cache[ap_mac] = "offline"

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
