# Madrid Activities Bot

This bot automatically collects and shares weekly activities and events in Madrid, Spain. It uses the Perplexity API to gather information and sends updates via Telegram.

## Features

- Weekly updates of Madrid events and activities
- Categorizes events by weekday and weekend
- Includes upcoming major events for the next 6 months
- Automated delivery via Telegram
- Runs automatically every Monday at 6 PM Madrid time

## Setup

1. Clone the repository:
```bash
git clone https://github.com/martinabrandsco/madrid-activities.git
cd madrid-activities
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```bash
cp .env.example .env
```

4. Add your credentials to the `.env` file:
- `PERPLEXITY_API_KEY`: Your Perplexity API key
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID

## GitHub Actions Setup

1. Go to your repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add the following secrets:
   - `PERPLEXITY_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

## Running Locally

```bash
python activities.py
```

## License

MIT License 