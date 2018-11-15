# from telegram.ext import Updater, CommandHandler
TOKEN = '623741444:AAEU_loDCnHYYWtSGKnH6sv3w3MdK5QbhLg'

updater = Updater(TOKEN)


def main():
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.start_polling()
    updater.idle()


def hello(bot, update):
    update.message.reply_text(
        f'Hello {update.message.from_user.first_name}!')


if __name__ == '__main__':
    main()