[![Build Status](https://github.com/dgonzalesjr/flipbot/actions/workflows/main.yml/badge.svg)](https://github.com/dgonzalesjr/flipbot/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/dgonzalesjr/flipbot.svg)](https://github.com/dgonzalesjr/flipbot/issues)
[![Stars](https://img.shields.io/github/stars/dgonzalesjr/flipbot.svg)](https://github.com/dgonzalesjr/flipbot/stargazers)
[![Forks](https://img.shields.io/github/forks/dgonzalesjr/flipbot.svg)](https://github.com/dgonzalesjr/flipbot/network)


# 🌀 FlipBot

FlipBot is an automated arbitrage assistant that monitors eBay listings for undervalued Pokémon cards and sends alerts to a Discord channel with "Buy Now" buttons for quick flipping opportunities. Stripe integration is included for future purchase flows.

## 🔧 Features

- 🔍 Scrapes live eBay listings based on keyword and price criteria
- 🧠 AI-powered parsing and buyer-match logic
- 💬 Discord embed alerts with clickable buttons
- 💾 Logs matches to CSV
- 💳 Stripe integration ready (test mode)

## 📦 Installation

```bash
git clone https://github.com/dgonzalesjr/flipbot.git
cd flipbot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🛠 Setup

Create a `.env` file at the project root:

```
OPENAI_API_KEY=sk-...
DISCORD_WEBHOOK=...
DISCORD_BOT_TOKEN=...
STRIPE_SECRET_KEY=...
EBAY_APP_ID=...
```

## ▶️ Usage

Run the main pipeline:

```bash
python main.py
```

Test Discord notifier:

```bash
python test_notifier.py
```

Run the eBay scraper only:

```bash
python scrape_ebay.py
```

## 📈 Roadmap

- [ ] Auto-purchase with Stripe Checkout
- [ ] Web dashboard for listing review
- [ ] Marketplace flip analytics

## 🤝 Contributing

Pull requests welcome! Please open an issue first for discussion.

## 📄 License

MIT © [Daniel Gonzales Jr.](https://github.com/dgonzalesjr)
