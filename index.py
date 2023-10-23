import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from decouple import config

TOKEN = config('TOKEN')
COINGECKO_API_URL = config('COINGECKO_API_URL')
COINGECKO_API_KEY = config('COINGECKO_API_KEY')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Cryptocurrency Bot. Use /crypto to get cryptocurrency prices.")

async def send_crypto_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the list of cryptocurrencies you want to display
    cryptocurrencies = ['bitcoin', 'ethereum', 'ripple', 'litecoin']

    prices = get_crypto_prices(cryptocurrencies)

    if prices is not None:
        response = "Cryptocurrency Prices:\n"
        for symbol, price in prices.items():
            response += f"{symbol}: ${price}\n"
    else:
        response = "Failed to retrieve cryptocurrency prices."

    await update.message.reply_text(response)

def get_crypto_prices(cryptos):
    params = {
        'ids': ','.join(cryptos),
        'vs_currencies': 'usd',
    }
    headers = {
        'Accept': 'application/json',
    }

    response = requests.get(COINGECKO_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        prices = {crypto: data[crypto]['usd'] for crypto in cryptos}
        return prices
    else:
        return None

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    crypto_handler = CommandHandler('crypto', send_crypto_prices)
    application.add_handler(start_handler)
    application.add_handler(crypto_handler)

    application.run_polling()
