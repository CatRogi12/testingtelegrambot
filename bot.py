import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Set your API keys and BTC address
TELEGRAM_TOKEN = '7691901346:AAGGlVKI9ca7FY_vxJ1a_GcoaAbYlusaOqY'
BTC_ADDRESS = 'bc1qsutpagav5h736x7qput7lmeyxpqz0ygdtyfke6'

# Function to get current BTC to USD conversion rate
def get_btc_price_in_usd():
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice/USD.json")
    data = response.json()
    return float(data["bpi"]["USD"]["rate"].replace(",", ""))

# Start command handler
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Test ($10)", callback_data="10")],
        [InlineKeyboardButton("Month ($1200)", callback_data="1200")],
        [InlineKeyboardButton("Lifetime ($6000)", callback_data="6000")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose a subscription option:", reply_markup=reply_markup)

# Button press handler
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    usd_amount = int(query.data)  # amount in USD based on button click
    btc_price = get_btc_price_in_usd()  # get latest BTC price
    btc_amount = usd_amount / btc_price  # calculate BTC equivalent

    response_text = (
        f"To proceed with the {usd_amount} USD option, please send exactly *{btc_amount:.6f} BTC* "
        f"to the following Bitcoin address:\n\n"
        f"`{BTC_ADDRESS}`\n\n"
        f"Current exchange rate: 1 BTC = ${btc_price:.2f} USD"
    )
    query.edit_message_text(text=response_text, parse_mode="Markdown")

def main():
    # Set up the Updater and dispatcher
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
