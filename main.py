import os, time, requests
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TARGET_URL = os.environ.get("TARGET_URL", "").strip()
KEYWORDS = [x.strip().lower() for x in os.environ.get("ALERT_KEYWORDS", "book tickets,available,coming soon").split(",")]
INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))

bot = Bot(TOKEN)
last_state = None

def check_page():
    if not TARGET_URL:
        return "No monitoring URL configured."
    r = requests.get(TARGET_URL, timeout=25, headers={"User-Agent":"Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    text = " ".join(soup.stripped_strings).lower()
    matches = [k for k in KEYWORDS if k in text]
    return "|".join(matches) or "none"

def main():
    global last_state
    bot.send_message(chat_id=CHAT_ID, text="🎬 Movie alert bot started. Checking every minute.")
    while True:
        try:
            state = check_page()
            if state != last_state and state != "none":
                bot.send_message(chat_id=CHAT_ID, text=f"🎟️ Movie page changed / alert keyword detected!\nMatched: {state}\n\nCheck booking page: {TARGET_URL}")
            last_state = state
        except Exception as e:
            print("Check error:", repr(e))
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
