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

NO, YES = range(2)
START_ROUTES, END_ROUTES = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with category buttons if they exist,
        otherwise asks to add category"""
    user_id = update.message.from_user['id']
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


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    """Checks if the command used right and adds category to the databse,
       otherwise shows the message how to use it right.
       Then asks user if that is what he/she/other wanted to add as their
       category name and adds if yes, sends how to use /add command reminder again
       if no"""
    # TODO can I put this user_id and cat_name to the db_worker functions I wonder
    cat_name = update.message.text.partition(' ')[2]
    user_id = update.message.from_user['id']
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data=str(YES)),
            InlineKeyboardButton("No", callback_data=str(NO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if cat_name:
        await update.message.reply_text(f'Do you want to add {cat_name}', reply_markup=reply_markup)
        return START_ROUTES
        # if setcat(cat_name, user_id):
        #     await update.message.reply_text(f'{cat_name} is added to your category list.')
        # else:
        #     await update.message.reply_text('Such a category already exist. Use /list to see all your categories.')

    else:
        await update.message.reply_text("Usage: /add <category>")


async def add_positive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await update.message.reply_text('Confirmed')


async def add_negative(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await update.message.reply_text('Denied')


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(add_positive, pattern='^' + str(YES) + '$')
            ],
            END_ROUTES: [
                CallbackQueryHandler(add_negative, pattern='^' + str(NO) + '$')
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add))

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    application.run_polling()