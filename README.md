# Job Tracker

Watches company career pages and job boards for openings matching your profile,
and notifies you on Telegram when a new one shows up.

## What it covers right now

- **Direct company scrapers (Workday)**: Philips, Siemens Healthineers, GE HealthCare
- **Job boards**: LinkedIn (public guest search, no login needed)
- **Naukri**: wired up but needs a one-time setup step from you (see below)
- **Indeed**: not included — Indeed no longer has a free/stable way to pull listings
  without a paid scraping service. Can be added later if you want to pay for that.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a Telegram bot (skip if reusing the one from your Hot Wheels tracker):
   - Message [@BotFather](https://t.me/BotFather) on Telegram, `/newbot`, follow prompts
   - Get your chat ID by messaging your bot, then visiting
     `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`

3. Test locally:
   ```
   set TELEGRAM_BOT_TOKEN=your_token
   set TELEGRAM_CHAT_ID=your_chat_id
   python main.py
   ```
   (use `export` instead of `set` on Mac/Linux)

4. Push this repo to GitHub, then add the two values above as repo secrets:
   Settings → Secrets and variables → Actions → New repository secret
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

5. The workflow in `.github/workflows/job_tracker.yml` runs every 6 hours automatically.
   You can also trigger it manually from the Actions tab.

## Enabling Naukri

Naukri's search API requires a header (`nkparam`) that Naukri's own frontend
generates dynamically. To capture a working one:

1. Open a Naukri search results page in Chrome, e.g.
   `https://www.naukri.com/qa-automation-engineer-jobs-in-bengaluru`
2. Open DevTools → Network tab → filter "Fetch/XHR" → reload the page
3. Find the request to `jobapi/v3/search`, right-click → Copy → Copy as cURL
4. Paste the `nkparam`, `appid`, and `systemid` header values into
   `scrapers/naukri.py`'s `FIXED_HEADERS` dict

Heads up: this header may need to be refreshed periodically if Naukri rotates it,
since it isn't a long-lived credential like BigBasket's cookies were.

## Adding more companies

Most large companies run on one of a few ATS platforms. If a company you want
to track uses Workday, just add it to `WORKDAY_COMPANIES` in `config.py` —
no new code needed. To find a company's Workday tenant/site, search
`"<company> careers myworkdayjobs.com"` and look at the URL structure:
`https://{tenant}.wd{n}.myworkdayjobs.com/{site}`

Dell, Cisco, Bosch, and Intel are worth checking next — they're commonly on
Workday or SuccessFactors too.

## Tuning matches

Edit `config.py`:
- `TARGET_TITLES` — job title keywords to match
- `SKILL_KEYWORDS` — used to surface which of your skills a posting mentions
- `TARGET_LOCATIONS` — locations to accept
- `LINKEDIN_SEARCHES` — which keyword/location combos to search on LinkedIn
- `WORKDAY_COMPANIES` — which company career sites to check
