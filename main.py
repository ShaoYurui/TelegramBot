TELEGRAM_BOT_TOKEN = "1497002692:AAGZ15U0t9ymCg7C4kQgUMUOwetWAG5ahFg"
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def sell(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}, please be reminded that due to COVID-19, please wash your clothes before passing it to buyers')

updater = Updater(TELEGRAM_BOT_TOKEN)

updater.dispatcher.add_handler(CommandHandler('sell', sell))

updater.start_polling()
updater.idle()