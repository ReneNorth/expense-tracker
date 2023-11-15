from telegram import (Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (ApplicationBuilder, Application, CommandHandler, ContextTypes,
                          PrefixHandler, MessageHandler, filters, Updater, ConversationHandler)
import os
import logging
import requests
from typing import List, NamedTuple, Optional
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
log = logging.getLogger(__name__)

TOKEN = os.getenv('TG_BOT_TOKEN')


MAIN_MENU_KEYBOARD: list = [
    ['/rate_on_date'],
    ['/rate_for_month'],
    ['/rate_year_to_date'],
    ['/update', '/start', '/cancel'],
]


class BotStates():
    MESSAGE = 'MESSAGE'
    CATEGORY = 'CATEGORY'


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


def get_category_keyboard() -> List[InlineKeyboardButton]:
    # теперь сюда положить категорию
    line = []
    buttons = [line]
    for i in range(0, 3):
        line.append(InlineKeyboardButton(f'{i}', callback_data=f'test {i}'))
    log.info(buttons)
    return buttons


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if add_expense_db(parse_expense(update.message.text)) == 'ok':
        log.info('it is ok')
        await update.message.reply_text('забрал и положил затрату в таблицу')
        return BotStates.CATEGORY
    return ConversationHandler.END


async def choose_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.info('we are in the category')
    keyboard = get_category_keyboard()
    log.info(keyboard)
    await update.message.reply_text(text='выбери категорию',
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    update.message.reply_text('тест прошел успешно')
    return ConversationHandler.END


async def cancel(update: Update) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, add_expense),
        ],
        states={
            BotStates.CATEGORY: [MessageHandler(
                filters.TEXT, choose_category)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=False
    ))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
