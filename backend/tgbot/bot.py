from telegram import (Update, ForceReply, InlineKeyboardButton,
                      InlineKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters,
                          ConversationHandler, CallbackQueryHandler)
import os
import logging
from exeptions import WrongName
import requests
from typing import List
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from messages import Message
from pathlib import Path

from helpers import convert_last_element_to_number


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / 'infra/.env')

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
HOST = os.getenv("HOST", default="http://127.0.0.1:8000/")
ALLOWED_CURRENCIES = ['usd', 'eur', 'rub', 'kzt']


@dataclass
class Expense:
    """Structure of an expense"""
    description: str
    amount: int
    who_paid: int = None
    category: int = None
    currency: str = None
    is_considered_debt: bool = True

    @classmethod
    def set_default_currency(cls, new_currency):
        expense_allowed_currencies = ALLOWED_CURRENCIES
        if new_currency in expense_allowed_currencies:
            cls._default_currency = new_currency
        else:
            print(f"{new_currency} is not a valid currency.")  # refactor

    def set_category(self, category):
        self.category = category

    def set_currency(self, currency):
        self.currency = currency

    def __post_init__(self):
        # Set default currency when an object is created
        self.currency = self._default_currency if hasattr(
            self, '_default_currency') else 'kzt'


class BotStates():
    MESSAGE = 'MESSAGE'
    SUGGEST_CATEGORY = 'SUGGEST_CATEGORY'
    SET_CATEGORY = 'SET_CATEGORY'
    ADD_EXPENSE = 'ADD_EXPENSE'
    ADD_CATEGORY_STATE = 'ADD_CATEGORY'


def add_expense_db(expense) -> str:
    request_body = asdict(expense)
    response = requests.post(url=f"{HOST}api/v1/expenses/",
                             json=request_body)
    if response.status_code == (201 or 200):  # refactor
        return 'ok'


def parse_expense(message: str) -> Expense:
    expense_list = message.split()
    match expense_list[0].lower():
        case 'д' | 'даша' | 'даш':
            who_paid = 1
            expense_list.pop(0)
        case 'ю' | 'юра' | 'юр' | 'юрий':
            who_paid = 2
            expense_list.pop(0)
        case _:
            raise WrongName(
                'possible options are д | даша | даш / ю | юра | юр | юрий')
    log.info('expense list before ifs', expense_list)
    if convert_last_element_to_number(expense_list[-1]) is None:
        currency = expense_list.pop(-1)
    amount = expense_list.pop(-1)
    new_expense = Expense(
        description=' '.join(expense_list),
        amount=amount,
        who_paid=who_paid)
    new_expense.set_currency(currency)
    return new_expense


def get_category_keyboard() -> List[InlineKeyboardButton]:
    response = requests.get(f'{HOST}/api/v1/categories')
    line = []
    categories = response.json()
    buttons = [line]
    for i in range(0, len(categories)):
        line.append(InlineKeyboardButton(
            text=f'{categories[i].get("name")}',
            callback_data=f'{categories[i].get("id")}'
        ))
    return buttons


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hi!',  # add instruction on how to use the bot
    )


async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE
                      ) -> ConversationHandler.END:
    try:
        parsed_message = parse_expense(update.message.text)
        log.info('после распарса сообщения')
        log.info(parsed_message)
    except WrongName as e:
        log.warning(f'something went wrong {e}')
        await update.message.reply_text('необрабатываемое исключение')
        return ConversationHandler.END
    context.chat_data['expense'] = parsed_message

    keyboard = get_category_keyboard()
    await update.message.reply_text(
        text='pick a category',
        reply_markup=InlineKeyboardMarkup(keyboard))
    return BotStates.SET_CATEGORY


async def how_to_add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='напиши название категории одним словом, и я добавлю её в список категррий')
    return BotStates.ADD_CATEGORY_STATE


async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info('working here')
    log.info(reply)
    reply = update.message.text

    log.info('логирую категорию из сообщения', reply)
    response = requests.post(url=f"{HOST}api/v1/categories/",
                             json={"name": reply})
    await update.message.reply_text('Добавил категорию')
    return ConversationHandler.END


async def set_default_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=f'{context.chat_data}',
                                    reply_markup=InlineKeyboardMarkup([[ALLOWED_CURRENCIES]]))

    Expense.set_default_currency(update.message.text)
    update.message.reply_text(text=Message.update_currency)
    return None


async def set_category(update: Update, context: ContextTypes.DEFAULT_TYPE
                       ) -> ConversationHandler.END:
    query = update.callback_query
    context.chat_data['expense'].set_category(query.data)
    log.info(context.chat_data['expense'])
    add_expense_db(context.chat_data['expense'])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='добавил расход',)
    return ConversationHandler.END


async def cancel(update: Update) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(text='the conversation has ended')
    return ConversationHandler.END


def main() -> None:
    """Starts the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler(
        'set_currency', set_default_currency))

    application.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler(
                'add_category', how_to_add_category),
        ],
        states={
            BotStates.ADD_CATEGORY_STATE: [MessageHandler(filters.TEXT, add_category)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=False
    ))

    application.add_handler(ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.TEXT, add_expense),
        ],
        states={
            BotStates.SET_CATEGORY: [CallbackQueryHandler(set_category)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=False
    ))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
