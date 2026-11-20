Movie Telegram alert bot scaffold

This is a basic page-change/keyword monitor. It is not a guaranteed BookMyShow availability detector.
Many ticket sites render show information in JavaScript, block automated requests, or restrict scraping.
Use only a page/source you are permitted to monitor.

Railway setup:
1. Upload these files to a GitHub repository.
2. Deploy that repository to Railway as a worker.
3. Set environment variables in Railway:
   TELEGRAM_TOKEN = your newly rotated BotFather token
   TELEGRAM_CHAT_ID = your Telegram chat ID
   TARGET_URL = the ticket page URL you want to monitor
   CHECK_INTERVAL = 60
   ALERT_KEYWORDS = book tickets,available,coming soon
4. Ensure the bot is started once in Telegram so it can send you messages.

Do not commit secrets or your token to GitHub.
