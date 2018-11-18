import importlib, plugin_list, sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Bot:
    def __init__(self, TOKEN):
        self.plugins = []
        self.updater = Updater(TOKEN)
        self.__setup()


    def start(self):
        self.updater.start_polling()
        self.updater.idle()


    def stop(self, bot, update):
        update.message.reply_text("Stopping bot.")
        print('stopping bot.')
        self.updater.stop()


    def __manage_plugins(self, bot, update):
        text = 'Installed plugins:'
        for plugin in plugin_list.plugins:
            text = text + '\n- ' + plugin
        update.message.reply_text(text)


    def __setup(self):
        # Setup hardcoded handlers
        self.updater.dispatcher.add_handler(CommandHandler('stop', self.stop))
        self.updater.dispatcher.add_handler(CommandHandler('plugins', self.__manage_plugins))
        
        # Add the plugins folder to the path list for module lookups
        sys.path.insert(0, './plugins')

        # Initialize plugins
        for plugin in plugin_list.plugins:
            print(f'hey! now loading: {plugin}')
            self.plugins.append(getattr(importlib.import_module(plugin, "plugins"), plugin)())
            # print(f'result: {self.plugins}')
        # TODO: Implement plugin checking
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.__on_text))

        # Register plugin handlers
        for plugin in self.plugins:
            for command, function in plugin.commands.items():
                print(command, function)
                self.updater.dispatcher.add_handler(CommandHandler(command, function))


    def __on_text(self, bot, update):
        # import pdb; pdb.set_trace()
        for plugin in self.plugins:
            print(f"--- executing for {plugin} ---")
            try:
                print(f"calling on_text for: {plugin}")
                plugin.on_text(bot, update)
            except Error:
                print("Oops.")
        print('finished execution of __on_text')




if __name__ == '__main__':
    bot = Bot('623741444:AAGVjDkeWiHxC6uMyH2ODDb9chfAl3Xw6AA')
    bot.start()

