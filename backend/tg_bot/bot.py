from telegram import Update, ForceReply
from telegram.ext import (ApplicationBuilder, Application, CommandHandler, ContextTypes,
                          PrefixHandler, MessageHandler, filters, Updater)
import os
import logging
import requests
from dotenv import load_dotenv

# from expenses.config import DEFAULT_CURRENCY

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


TOKEN = os.getenv('TG_BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


def add_expense_db(expense):
    response = requests.post(url="http://127.0.0.1:8000/api/v1/expenses/",
                             data=expense)
    print(response)
    if response.status_code == (201 or 200):
        return 'ok'


def parse_expense(message: str):
    # returns json
    print(message)

    expense_list = message.split()

    if expense_list[0] == 'д':
        who_paid = 1
    if expense_list[0] == 'ю':
        who_paid = 2
    if len(expense_list) >= 7:
        currency = expense_list[6]
    if len(expense_list) < 7:
        currency = 'kzt'

    expense = {
        "description": expense_list[1],
        "amount": expense_list[2],
        "category": expense_list[3],
        "currency": currency,
        "who_paid": who_paid}

    return expense


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if add_expense_db(parse_expense(update.message.text)) == 'ok':
        await update.message.reply_text('забрал и положил затрату в таблицу')


# app = ApplicationBuilder().token(TOKEN).build()

# app.add_handler(PrefixHandler(['д', 'ю'], 'test', add_expense))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, add_expense))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
