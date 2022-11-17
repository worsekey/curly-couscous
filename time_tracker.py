from db_worker import setcat, delcat, listcat, stopcat, startcat
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          MessageHandler,
                          ContextTypes,
                          ConversationHandler,
                          CallbackQueryHandler)
from telegram import (Update,
                      KeyboardButton,
                      ReplyKeyboardMarkup,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      )
from secret import TOKEN
from filters import stopfilter, startfilter
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show list of cats if not new user, tell /add <category> if new user"""
    user_id = update.message.from_user['id']
    cat_list = listcat(user_id)
    if cat_list:
        cats = '\n'.join(cat_list)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your categories are:\n\n{cats}\n\n'
                                                                              f'Use /begin <category> '
                                                                              f'to start time tracking ')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="You have nothing to track yet, "
                                            "use /add <category> to set up a category to track time for")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Checks if the command used right and adds category to the database,
       otherwise shows the message how to use it right.
       Then asks user if that is what he/she/other wanted to add as their
       category name and adds if yes, sends how to use /add command reminder again
       if no"""
    # TODO can I put this user_id and cat_name to the db_worker functions I wonder
    cat_name = update.message.text.partition(' ')[2]
    user_id = update.message.from_user['id']

    if cat_name:
        if setcat(cat_name, user_id):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{cat_name} added.\n'
                                                                                  f'To start tracking use\n\n '
                                                                                  f'/begin {cat_name}')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{cat_name} already exist.\n'
                                                                                  f'To start tracking {cat_name} use \n\n'
                                                                                  f'/begin {cat_name}\n\n'
                                                                                  f'Or /add another category.')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Usage: /add <category>')


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_name = update.message.text.partition(' ')[2]
    user_id = update.message.from_user['id']
    if cat_name:
        msg = delcat(cat_name, user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Usage: /del <category>\n'
                                                                              'All your categories '
                                                                              'available by command /list')


async def list_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user['id']
    cat_list = listcat(user_id)
    if cat_list:
        cats = '\n'.join(cat_list)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Your categories are\n\n{cats}\n\n'
                                                                              f'To start tracking one of them use\n'
                                                                              f'/begin <category>')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You don't have categories yet.\n"
                                                                              "start by adding at least one with\n"
                                                                              "/add <category>")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add))
    application.add_handler(CommandHandler('del', delete))
    application.add_handler(CommandHandler('list', list_cat))

    application.run_polling()