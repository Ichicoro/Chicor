import importlib, sys, json, utils
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Bot:
    def __init__(self):
        self.plugins = []
        self.config = []
        try:
            self.config = json.load(open('config.json', 'r'));
        except IOError:
            utils.generate_config_file()
            print('Configuration file (config.json) not found. Sample file has been created.')
        
        # Check the settings file for relevant info
        if self.__validate_config()!=0:
            raise ValueError

        # Setup the bot
        self.__setup()


    # This method validates a config object (read from a decoded json file)
    def __validate_config(self):
        try:
            self.updater = Updater(self.config['TELEGRAM_API_TOKEN'])
        except Exception:
            utils.pprint('Missing API token! Write it in the config.json file')
            return -1;
        try:
            self.plugin_list = self.config['plugin_list']
        except Exception:
            utils.pprint('Missing plugin list. Set it up in the config.json file')
            return -1;
        return 0;


    def __fix_plugin_config_settings(self):
        for plugin in self.config.plugin_list:
            if plugin not in self.config.plugin_settings:
                if 

    def start(self):
        self.updater.start_polling()
        self.updater.idle()


    def stop(self):
        update.message.reply_text("Stopping bot.")
        print('stopping bot.')
        self.updater.stop()


    def __manage_plugins(self, bot, update):
        text = 'Installed plugins:'
        for plugin in self.plugin_list.plugins:
            text = text + '\n- ' + plugin
        update.message.reply_text(text)


    def __setup(self):
        # Setup hardcoded handlers
        self.updater.dispatcher.add_handler(CommandHandler('stop', self.stop))
        self.updater.dispatcher.add_handler(CommandHandler('plugins', self.__manage_plugins))
        
        # Add the plugins folder to the path list for module lookups
        sys.path.insert(0, './plugins')

        # Initialize plugins
        for plugin in self.plugin_list:
            print(f'hey! now loading: {plugin}')
            self.plugins.append(getattr(importlib.import_module(plugin, "plugins"), plugin)())

        # TODO: Implement plugin checking
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.__on_text))

        # Register plugin handlers
        for plugin in self.plugins:
            for command, function in plugin.commands.items():
                print(command, function)
                self.updater.dispatcher.add_handler(CommandHandler(command, function))


    def __on_text(self, bot, update):
        for plugin in self.plugins:
            try:
                print(f"calling on_text for: {plugin}")
                plugin.on_text(bot, update)
            except Error:
                print("Oops.")
        print('finished execution of __on_text')




if __name__ == '__main__':
    bot = Bot()
    bot.start()

