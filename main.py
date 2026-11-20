import asyncio
import os
from bs4 import BeautifulSoup
from curl_cffi import requests
from telegram import Bot

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TARGET_URL = os.environ.get("TARGET_URL", "").strip()
PROXY_URL = os.environ.get("PROXY_URL", "").strip()
KEYWORDS = [
    x.strip().lower()
    for x in os.environ.get("ALERT_KEYWORDS", "avengers doomsday,doomsday").split(",")
    if x.strip()
]
INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))

bot = Bot(TOKEN)
last_state = None

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-IN,en-US;q=0.9,en;q=0.8",
    "Referer": "https://in.bookmyshow.com/",
}


def check_page():
    if not TARGET_URL:
        return "No monitoring URL configured."
    proxies = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
    r = requests.get(
        TARGET_URL,
        impersonate="chrome",
        headers=HEADERS,
        proxies=proxies,
        timeout=25,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    text = " ".join(soup.stripped_strings).lower()
    matches = [k for k in KEYWORDS if k in text]
    return "|".join(matches) or "none"


async def main():
    global last_state
    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"🎬 Movie alert bot started. Checking every {INTERVAL} seconds.",
    )
    while True:
        try:
            state = await asyncio.to_thread(check_page)
            print("Check OK, matched:", state, flush=True)
            if state != last_state and state != "none":
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=(
                        f"🎟️ Movie page changed / alert keyword detected!\n"
                        f"Matched: {state}\n\n"
                        f"Check booking page: {TARGET_URL}"
                    ),
                )
            last_state = state
        except Exception as e:
            print("Check error:", repr(e), flush=True)
        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
    
