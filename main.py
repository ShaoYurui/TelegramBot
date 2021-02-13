TELEGRAM_BOT_TOKEN = "1497002692:AAGZ15U0t9ymCg7C4kQgUMUOwetWAG5ahFg"
from time import sleep
import datetime
from telegram import Update,Message
from telegram.ext import Updater, CommandHandler,ConversationHandler, CallbackContext, MessageHandler, Filters, JobQueue
updater = Updater(TELEGRAM_BOT_TOKEN)
MY_CHAT_ID = 495295265
MY_CROUP_CHAT_ID = -503183212
WeWardrobe_CHAT_ID = -1001409782425


class ITEM:
    def __init__(self, name='NIL',price=0,photo='NIL',seller='NIL',index=0,info='NIL',msg_id = 0):
        self.name = name
        self.message_id = msg_id
        self.price = price
        self.photo = photo
        self.seller = seller
        self.index = index
        self.info = info


items_list = []
items_sold = []
waste_msg_list = []
pre_reminder = 0
no_listing = 0
no_sold = 0
roll_stop = 0
started = 0
availability = 1


def sell(update : Update, context : CallbackContext) -> int:
    global availability
    if availability:
        availability = 0
    else:
        return ConversationHandler.END
    global no_listing
    no_listing += 1
    waste_msg_list.append(update.effective_message.message_id)
    tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"/cancel to cancel").message_id
    waste_msg_list.append(tmp)
    tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi @{update.effective_user.username}\nwhat product are you selling?\n(e.g. jeans,black jacket...)").message_id
    waste_msg_list.append(tmp)

    items_list.append(ITEM(index=no_listing))
    return PRODUCT_NAME


def product_name(update : Update, context : CallbackContext) -> int:
    items_list[-1].name = update.message.text
    waste_msg_list.append(update.effective_message.message_id)
    tmp = context.bot.send_message( chat_id=update.effective_chat.id,
                              text=f"@{update.effective_user.username}\nwhat is the price for [{items_list[-1].name}] ?").message_id
    waste_msg_list.append(tmp)
    return PRODUCT_PRICE


def product_price(update : Update, context : CallbackContext) -> int:
    waste_msg_list.append(update.effective_message.message_id)
    items_list[-1].price = update.message.text
    tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"@{update.effective_user.username}\n"
                                  f"please send [ONE] photo of your [{items_list[-1].name}] to the group for reference.").message_id
    waste_msg_list.append(tmp)
    return PRODUCT_PHOTO


def product_photo(update : Update, context : CallbackContext) -> int:
    waste_msg_list.append(update.effective_message.message_id)
    items_list[-1].seller = update.effective_user.username
    items_list[-1].photo = update.message.photo[-1].file_id
    tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                                   text = f"@{update.effective_user.username}, Do you want to add more information?\n"
                                          f"(e.g. size small, 9/10 new) ").message_id
    waste_msg_list.append(tmp)
    return PRODUCT_INFO


def product_info(update : Update, context : CallbackContext) -> int:
    global pre_reminder,availability
    waste_msg_list.append(update.effective_message.message_id)
    items_list[-1].info = update.message.text
    if update.effective_user.username == "yuruuii":
        tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                                                text="seller's name ?").message_id
        waste_msg_list.append(tmp)
        return PRODUCT_SELLER
    items_list[-1].message_id = context.bot.send_photo(chat_id=update.effective_chat.id, photo=items_list[-1].photo,
                           caption=f"[{items_list[-1].name}] for [{items_list[-1].price}]\n"
                                   f"info : {items_list[-1].info}\n"
                                   f"Please contact @{items_list[-1].seller} for more information").message_id

    if pre_reminder != 0:
        context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=pre_reminder)
    pre_reminder = context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please be reminded that due to COVID-19, please wash your clothes before passing it to buyers\nreply your item with /sold to remove your item").message_id
    for i in waste_msg_list:
        context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=f"{i}")
    waste_msg_list.clear()
    availability = 1

    return ConversationHandler.END


def product_seller(update : Update, context : CallbackContext) -> int:
    global pre_reminder,availability
    items_list[-1].seller = update.message.text
    waste_msg_list.append(update.effective_message.message_id)
    items_list[-1].message_id = context.bot.send_photo(chat_id=update.effective_chat.id, photo=items_list[-1].photo,
                                                       caption=f"[{items_list[-1].name}] for [{items_list[-1].price}]\n"
                                                               f"info : {items_list[-1].info}\n"
                                                               f"Please contact @{items_list[-1].seller} for more information").message_id
    if pre_reminder != 0:
        context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=pre_reminder)
    pre_reminder = context.bot.send_message(chat_id=update.effective_chat.id,
                                            text="Please be reminded that due to COVID-19, please wash your clothes before passing it to buyers\nreply your item with /sold to remove your item").message_id
    for i in waste_msg_list:
        context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=f"{i}")
    waste_msg_list.clear()
    availability = 1

    return ConversationHandler.END


def cancel(update : Update, context : CallbackContext) -> int:
    global no_listing, availability
    availability = 1
    tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                             text="canceled").message_id
    waste_msg_list.append(tmp)
    sleep(2)
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update._effective_message.message_id)
    for i in waste_msg_list:
        context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=f"{i}")
    items_list.pop(-1)
    no_listing -= 1
    waste_msg_list.clear()
    return ConversationHandler.END


def bg_data(update : Update, context : CallbackContext):
    context.bot.send_message(chat_id=MY_CROUP_CHAT_ID,
                             text=f"total number of items listed is {no_listing}")
    for i in range(len(items_list)):
        context.bot.send_photo(chat_id=MY_CROUP_CHAT_ID,photo=items_list[i].photo,
                               caption=f"id : {items_list[i].index}\nname : {items_list[i].name}\nprice : {items_list[i].price}\nseller: @{items_list[i].seller}")

    context.bot.send_message(chat_id=MY_CROUP_CHAT_ID,
                             text=f"total number of items sold is {no_sold}")
    for i in range(len(items_sold)):
        context.bot.send_photo(chat_id=MY_CROUP_CHAT_ID,photo=items_sold[i].photo,
                               caption=f"id : {items_sold[i].index}\nname : {items_sold[i].name}\nprice : {items_sold[i].price}\nseller: @{items_sold[i].seller}")
    context.bot.send_message(chat_id=MY_CROUP_CHAT_ID,
                             text=f"total number of items listed is {no_listing}")
    context.bot.send_message(chat_id=MY_CROUP_CHAT_ID,
                             text=f"total number of items sold is {no_sold}")


def remove(update : Update, context : CallbackContext):
    global no_listing
    if update.effective_user.username == "yuruuii":
        msg_id = update.effective_message.reply_to_message.message_id
        for i in range(len(items_list)):
            if items_list[i].message_id == msg_id:
                context.bot.deleteMessage(chat_id=update.effective_chat.id,
                                          message_id=update.effective_message.reply_to_message.message_id)
                context.bot.deleteMessage(chat_id=update.effective_chat.id,
                                          message_id=update.effective_message.message_id)
                items_list.pop(i)
                no_listing -= 1

    else:
        tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Only Admin can remove items").message_id
        sleep(3)
        context.bot.deleteMessage(chat_id=update.effective_chat.id,
                                  message_id=update.effective_message.message_id)
        context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=tmp)


def sold(update : Update, context : CallbackContext):
    global no_sold
    msg_id = update.effective_message.reply_to_message.message_id
    for i in range(len(items_list)):
        if items_list[i].message_id == msg_id:
            if items_list[i].seller == update.effective_user.username:
                items_sold.append(items_list[i])
                no_sold += 1
                tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Thank you for using RVRC Shared Closet").message_id
                context.bot.send_message(chat_id=MY_CROUP_CHAT_ID,
                                         text=f"The following item has been sold\ntotal number of item sold = [{no_sold}]")
                context.bot.forwardMessage(chat_id=MY_CROUP_CHAT_ID,from_chat_id=update.effective_chat.id,message_id=update.effective_message.reply_to_message.message_id)
                sleep(2)
                context.bot.deleteMessage(chat_id=update.effective_chat.id,
                                          message_id=update.effective_message.reply_to_message.message_id)
                context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=tmp)
                items_list.pop(i)

            else:
                tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Only the seller can change the status").message_id
                sleep(2)
                context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=tmp)
            context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
            return


def unknown(update : Update, context : CallbackContext):
    tmp = context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.").message_id
    sleep(5)
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=tmp)
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)


def roll_start(context : CallbackContext):
    if roll_stop == 1: return
    global pre_reminder
    if no_listing == 0 or len(items_list) == 0:
        context.bot.send_message(chat_id=MY_CHAT_ID, text="unable to roll as no_listing = 0")
        return
    tmp = items_list[0]
    items_list.pop(0)
    items_list.append(tmp)
    tmp = context.bot.send_photo(chat_id=WeWardrobe_CHAT_ID, photo=items_list[-1].photo,
                           caption=f"[{items_list[-1].name}] for [{items_list[-1].price}]\n"
                                   f"info : {items_list[-1].info}\n"
                                   f"Please contact @{items_list[-1].seller} for more information").message_id
    w = items_list[-1].message_id
    items_list[-1].message_id = tmp
    tmp = pre_reminder;
    pre_reminder = context.bot.send_message(chat_id=WeWardrobe_CHAT_ID,
                                            text="Please be reminded that due to COVID-19, please wash your clothes before passing it to buyers\nreply your item with /sold to remove your item").message_id
    context.bot.deleteMessage(chat_id=WeWardrobe_CHAT_ID, message_id=w)
    if tmp != 0:
        context.bot.deleteMessage(chat_id=WeWardrobe_CHAT_ID,message_id=tmp)



def roll(update : Update, context : CallbackContext):
    global roll_stop,started

    if roll_stop == 1:
        context.bot.send_message(chat_id=MY_CHAT_ID, text="rolling resume")
        roll_stop = 0
        return
    if started == 0:
        context.bot.send_message(chat_id=MY_CHAT_ID, text="start rolling")
        roll_start(context)
        context.job_queue.run_repeating(roll_start,interval=24*60*60)
        started = 1
    else :
        roll_start(context)


def stproll(update : Update, context : CallbackContext):
    global roll_stop
    context.bot.send_message(chat_id=MY_CHAT_ID, text="rolling paused")
    roll_stop = 1


def buy(update : Update, context : CallbackContext) :
    roll_start(context)
    tmp = context.bot.send_message(chat_id=update.effective_chat.id,
                             text="please directly contact the seller to buy").message_id
    sleep(5)
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=update._effective_message.message_id)
    context.bot.deleteMessage(chat_id=update.effective_chat.id,message_id=tmp)


PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_PHOTO,PRODUCT_INFO,PRODUCT_SELLER = range(5)
sell_process = ConversationHandler(
        entry_points=[CommandHandler('sell', sell)],
        states={
            PRODUCT_NAME: [MessageHandler(Filters.text & (~Filters.command), product_name)],
            PRODUCT_PRICE: [MessageHandler(Filters.text & (~Filters.command), product_price)],
            PRODUCT_PHOTO: [MessageHandler(Filters.photo & (~Filters.command), product_photo)],
            PRODUCT_INFO: [MessageHandler(Filters.text & (~Filters.command), product_info)],
            PRODUCT_SELLER: [MessageHandler(Filters.text & (~Filters.command), product_seller)],
        },
        fallbacks=[CommandHandler('cancel', cancel)])
updater.dispatcher.add_handler(sell_process)
updater.dispatcher.add_handler(CommandHandler('sold', sold))
updater.dispatcher.add_handler(CommandHandler('buy', buy))
updater.dispatcher.add_handler(CommandHandler('roll', roll))
updater.dispatcher.add_handler(CommandHandler('remove', remove))
updater.dispatcher.add_handler(CommandHandler('stproll', stproll))
updater.dispatcher.add_handler(CommandHandler('bbb', bg_data))
unknown_handler = MessageHandler(Filters.command, unknown)
updater.dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
