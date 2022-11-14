from db_worker import setcat, delcat, listcat, stopcat, startcat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram import (Update,
                      KeyboardButton,
                      ReplyKeyboardMarkup,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)
from secret import TOKEN
from filters import stopfilter, startfilter
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with category buttons if they exist,
        otherwise asks to add category"""
    user = update.message.from_user
    user_id = user['id']
    cat_list = listcat(user_id)
    if cat_list:
        keyboard = [
            [
                InlineKeyboardButton("Option option option option", callback_data="1"),
                InlineKeyboardButton("Option 2", callback_data="2"),
            ],
            [InlineKeyboardButton("Option 3", callback_data="3")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Use /add <category> to add name of activity you would like to track.")



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    #Handlers
    application.add_handler(CommandHandler('start', start))

    application.run_polling()