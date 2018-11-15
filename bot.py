from telegram.ext import Updater, CommandHandler


class Bot:
    def __init__(self, TOKEN):
        self.updater = Updater(TOKEN)

    def start(self):
        self.updater.dispatcher.add_handler(CommandHandler('hello', lambda bot, update: update.message.reply_text(
            f'Hello {update.message.from_user.first_name}!')))
        self.updater.start_polling()
        self.updater.idle()


if __name__ == '__main__':
    bot = Bot('623741444:AAEU_loDCnHYYWtSGKnH6sv3w3MdK5QbhLg')
    bot.start()

