TELEGRAM_BOT_TOKEN = "1497002692:AAGZ15U0t9ymCg7C4kQgUMUOwetWAG5ahFg"
from telegram import Update,Message
from telegram.ext import Updater, CommandHandler,ConversationHandler, CallbackContext, MessageHandler, Filters

updater = Updater(TELEGRAM_BOT_TOKEN)
tmp_name = "NULL"
tmp_seller="NULL"
tmp_price = "NULL"
tmp_photo_id = "NULL"
tmp_index = 0;
max_num =10;
no_listing = 0;
no_sold = 0;

class item:
    def __init__(self, name,price,photo,seller,index,info='NIL'):
        self.name = name
        self.price = price
        self.photo = photo
        self.seller = seller
        self.index = index
        self.info = info


itme_list= []

PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_PHOTO,PRODUCT_INFO = range(4)

def test_sample():
    global tmp_index,no_listing
    no_listing=3
    tmp_index=3
    itme_list.append(item(name="Jeans", price=10,
                          photo="AgACAgUAAxkBAAIGyl_x9232CVj9IVgxvmdUZIR3AAG7FQAC_6sxG6IwkVdyqYyqm3ORAeifwmx0AAMBAAMCAAN5AANcxQUAAR4E",
                          seller="yuruuii", index=0))
    itme_list.append(item(name="Dress", price=90,
                          photo="AgACAgUAAxkBAAIG11_x95zjElmJo3aVzrAFUS83wHNXAAJeqzEbD8GJV7ytHUv4QnNQ1oxlbHQAAwEAAwIAA3kAA9MFBwABHgQ",
                          seller="yuruuii", index=1))
    itme_list.append(item(name="Jacket", price=10,
                          photo="AgACAgUAAxkBAAIG4F_x967NhJFh6UJ7DJT7FxA1sa4GAALWqzEbfcOJVyDIgnTARKpBCdlFbXQAAwEAAwIAA3kAA1MyAgABHgQ",
                          seller="yuruuii", index=2))


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
    context.bot.send_message(chat_id=update.effective_chat.id,text = f"@{update.effective_user.username}, Do you want to add more information?\n(e.g. size small, 9/10 new) ")
    return PRODUCT_INFO

def product_info(update : Update, context : CallbackContext) -> int:
    global tmp_index, tmp_photo_id, tmp_seller, no_listing
    tmp_info = update.message.text
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=tmp_photo_id,
                           caption=f"Dear @{update.effective_user.username}\nyou are selling 【{tmp_name}】 for 【{tmp_price}】\ninfo : {tmp_info}")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please be reminded that due to COVID-19, please wash your clothes before passing it to buyers")
    itme_list.append(item(name=tmp_name, price=tmp_price, photo=tmp_photo_id, seller=tmp_seller, index=tmp_index, info = tmp_info))
    if (tmp_index == max_num):
        itme_list.pop(0);
    else:
        tmp_index += 1
    no_listing += 1;
    return ConversationHandler.END

def cancel(update : Update, context : CallbackContext) -> int:
    update.message.reply_text("canceled")
    return ConversationHandler.END

def list(update : Update, context : CallbackContext):
    if tmp_index == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="No listing yet")
    for i in range(tmp_index):
        context.bot.send_photo(chat_id=update.effective_chat.id,photo=itme_list[i].photo,
                               caption=f"【{itme_list[i].name}】 for 【{itme_list[i].price}】\ninfo : {itme_list[i].info}\nplease DM @{itme_list[i].seller} for more information")

def sold(update : Update, context : CallbackContext):
    global no_sold
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Thank you for using RVRC Shared Closet")
    no_sold += 1

def remove(update : Update, context : CallbackContext):
    global tmp_index
    target = str(update.message.text)
    target=target.replace('/remove','')
    target=target.replace(' ', '')

    if target == '':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="please re-type with item id")
        return
    target=int(target)
    if target<tmp_index:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=itme_list[target].photo,
                               caption=f"item[{target}] removed")
        itme_list.pop(target)
        tmp_index -= 1
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="please check item id")

def bg_data(update : Update, context : CallbackContext):
    if tmp_index == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="No listing yet")
    for i in range(tmp_index):
        context.bot.send_photo(chat_id=update.effective_chat.id,photo=itme_list[i].photo,
                               caption=f"id : {itme_list[i].index}\nname : {itme_list[i].name}\nprice : {itme_list[i].price}\nseller: @{itme_list[i].seller}")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"total number of items listed is {no_listing}")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"total number of items sold is {no_sold}")

test_sample()

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('sell', sell)],
        states={
            PRODUCT_NAME: [MessageHandler(Filters.text & (~Filters.command), product_name)],
            PRODUCT_PRICE: [MessageHandler(Filters.text & (~Filters.command), product_price)],
            PRODUCT_PHOTO: [MessageHandler(Filters.photo & (~Filters.command), product_photo)],
            PRODUCT_INFO: [MessageHandler(Filters.text & (~Filters.command), product_info)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(CommandHandler('list',list))
updater.dispatcher.add_handler(CommandHandler('buy',list))
updater.dispatcher.add_handler(CommandHandler('sold',sold))
updater.dispatcher.add_handler(CommandHandler('remove',remove))
updater.dispatcher.add_handler(CommandHandler('bbb',bg_data))

updater.start_polling()
updater.idle()