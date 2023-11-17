from telegram import (Update, ForceReply, InlineKeyboardButton,
                      InlineKeyboardMarkup)
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
ALLOWED_CURRENCIES = ['usd', 'eur', 'rub', 'kzt']


@dataclass
class Expense:
    """Structure of an expense"""
    description: str
    amount: int
    who_paid: int = 1
    category: int = None
    currency: str = 'kzt'
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

    def __post_init__(self):
        # Set default currency when an object is created
        self.currency = self._default_currency if hasattr(
            self, '_default_currency') else 'kzt'


class BotStates():
    MESSAGE = 'MESSAGE'
    SUGGEST_CATEGORY = 'SUGGEST_CATEGORY'
    SET_CATEGORY = 'SET_CATEGORY'
    ADD_EXPENSE = 'ADD_EXPENSE'


def add_expense_db(expense):

    request_body = asdict(expense)
    log.info(type(request_body))

    log.info(request_body)
    response = requests.post(url="http://127.0.0.1:8000/api/v1/expenses/",
                             json=request_body)
    log.info(response.content)
    log.info(response.headers)
    if response.status_code == (201 or 200):
        return 'ok'


def parse_expense(message: str):
    expense_list = message.split()

    match expense_list[0]:
        case 'д':
            who_paid = 1
        case 'д':
            who_paid = 2
        case _:
            raise WrongName
    if len(expense_list) >= 7:
        currency = expense_list[6]
    if len(expense_list) < 7:
        currency = 'kzt'

    return Expense(
        description=expense_list[1],
        amount=expense_list[2],
        currency=currency,
        who_paid=who_paid)


def get_category_keyboard() -> List[InlineKeyboardButton]:
    line = []
    buttons = [line]
    for i in range(0, 3):
        line.append(InlineKeyboardButton(
            f'категория {i+1}',
            callback_data=i+1
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
    except WrongName as e:
        log.warning(f'something went wrong {e}')
        await update.message.reply_text('необрабатываемое исключение')
        return ConversationHandler.END
    context.chat_data['expense'] = parsed_message

    keyboard = get_category_keyboard()
    await update.message.reply_text(text=f'{context.chat_data}',
                                    reply_markup=InlineKeyboardMarkup(keyboard))
    return BotStates.SET_CATEGORY


async def add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


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
    add_expense_db(context.chat_data['expense'])
    return ConversationHandler.END


async def cancel(update: Update) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(text='the conversation has ended')
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler(
        "set_currency", set_default_currency))
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


if __name__ == "__main__":
    main()
