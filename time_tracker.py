from db_worker import setcat, delcat, listcat, stopcat, startcat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from secret import TOKEN
from filters import stopfilter, startfilter
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)




if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()


    application.run_polling()