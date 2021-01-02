TELEGRAM_BOT_TOKEN = "1497002692:AAGZ15U0t9ymCg7C4kQgUMUOwetWAG5ahFg"
from telegram import Update,Message
from telegram.ext import Updater, CommandHandler,ConversationHandler, CallbackContext, MessageHandler, Filters

updater = Updater(TELEGRAM_BOT_TOKEN)
tmp_name = "NULL"
tmp_seller="NULL"
tmp_price = "NULL"
tmp_index = 0;
tmp_photo_id = "NULL"
max_num =10;
no_listing = 0;
no_sold = 0;

class item:
    def __init__(self, name,price,photo,seller):
        self.name = name
        self.price = price
        self.photo = photo
        self.seller = seller

itme_list= []

PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_PHOTO = range(3)

def sell(update : Update, context : CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi @{update.effective_user.username}\nwhat product are you selling?\n(e.g. jeans,black jacket...)")
    return PRODUCT_NAME

def product_name(update : Update, context : CallbackContext) -> int:
    global tmp_name
    tmp_name = update.message.text
    context.bot.send_message( chat_id=update.effective_chat.id,
                              text=f"@{update.effective_user.username}\nwhat is the price for 【{tmp_name}】 ?")
    return PRODUCT_PRICE

def product_price(update : Update, context : CallbackContext) -> int:
    global tmp_price
    tmp_price = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"@{update.effective_user.username}\nplease send 【ONE】 photo of your 【{tmp_name}】 to the group for reference.")
    return PRODUCT_PHOTO

def product_photo(update : Update, context : CallbackContext) -> int:
    global tmp_index, tmp_photo_id, tmp_seller, no_listing
    tmp_seller = update.effective_user.username
    tmp_photo_id = update.message.photo[-1].file_id
    update.message.reply_text(f"Dear @{update.effective_user.username}\nyou are selling 【{tmp_name}】 for 【{tmp_price}】 .")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Please be reminded that due to COVID-19, please wash your clothes before passing it to buyers")

    if(tmp_index == max_num):
        itme_list.pop(0);
    else:
        tmp_index += 1
    itme_list.append(item(name = tmp_name, price = tmp_price, photo = tmp_photo_id, seller = tmp_seller))
    no_listing += 1;
    return ConversationHandler.END

def cancel(update : Update, context : CallbackContext) -> int:
    update.message.reply_text("canceled")
    return ConversationHandler.END

def list(update : Update, context : CallbackContext):
    for i in range(tmp_index):
        context.bot.send_photo(chat_id=update.effective_chat.id,photo=itme_list[i].photo,
                               caption=f"【{itme_list[i].name}】 for 【{itme_list[i].price}】\nplease DM @{itme_list[i].seller} for more information")

def bg_data(update : Update, context : CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"total number of items listed is {no_listing}")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"total number of items sold is {no_sold}")

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
updater.dispatcher.add_handler(CommandHandler('list',list))
updater.dispatcher.add_handler(CommandHandler('AY20G20B',bg_data))

updater.start_polling()
updater.idle()