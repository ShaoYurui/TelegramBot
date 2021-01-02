TELEGRAM_BOT_TOKEN = "1497002692:AAGZ15U0t9ymCg7C4kQgUMUOwetWAG5ahFg"
from telegram import Update,Message
from telegram.ext import Updater, CommandHandler,ConversationHandler, CallbackContext, MessageHandler, Filters

updater = Updater(TELEGRAM_BOT_TOKEN)
name = "NULL"
price = "NULL"

PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_PHOTO = range(3)

def sell(update : Update, context : CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hi @{update.effective_user.username}, what product are you selling? (e.g. jeans,black jacket...)")
    return PRODUCT_NAME

def product_name(update : Update, context : CallbackContext) -> int:
    global name
    name = update.message.text
    context.bot.send_message( chat_id=update.effective_chat.id, text=f"@{update.effective_user.username}, what is the price for {name} ?")
    return PRODUCT_PRICE

def product_price(update : Update, context : CallbackContext) -> int:
    global price
    price = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"@{update.effective_user.username}, please send ONE photo of your {name} to the group for reference.")
    return PRODUCT_PHOTO

def product_photo(update : Update, context : CallbackContext) -> int:
    update.message.reply_text(f"Dear @{update.effective_user.username}, you are selling {name} for {price} .")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Please be reminded that due to COVID-19, please wash your clothes before passing it to buyers")
    return ConversationHandler.END

def cancel(update : Update, context : CallbackContext) -> int:
    update.message.reply_text("canceled")
    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('sell', sell)],
        states={
            PRODUCT_NAME: [MessageHandler(Filters.text & (~Filters.command), product_name)],
            PRODUCT_PRICE: [MessageHandler(Filters.text & (~Filters.command), product_price)],
            PRODUCT_PHOTO: [MessageHandler(Filters.photo & (~Filters.command), product_photo)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()