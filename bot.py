#!/usr/bin/env python3
import importlib, sys, utils, logging, os, yaml
from utils import set_interval, get_admin_ids
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Bot:
    def __init__(self):
        self.plugins = []
        self.config = []
        self.version = "1.0.0"
        self.save_timer = None

        self.__upgrade_config()

        try:
            # self.config = json.load(open('config.json', 'r'));
            with open('config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except IOError:
            utils.generate_config_file()
            logging.warn('Configuration file (config.yaml) not found. Sample file has been created.')

        # Check and load the settings file
        if self.__validate_and_load_config() != 0:
            raise ValueError

        # Setup the bot
        self.__setup()


    # @set_interval(10)
    def __save_plugin_config(self, bot, job):
        for plugin in self.plugins:
            try:
                plugin_name = plugin.__class__.__name__
                logging.info(f'saving settings for {plugin_name}')
                self.config['plugin_settings'][plugin_name] = plugin.config
            except AttributeError:
                logging.error(f'wtf? No plugin.config for {plugin.__class__.__name__}')
        self.__save_config()


    # This method saves the config (self.config) to file (config.json)
    def __save_config(self):
        with open('config.yaml', 'w') as file:
            yaml.dump(self.config, file)
            # json.dump(self.config, file, indent=4, sort_keys=True)


    # Print plugin info to chat
    def __print_info(self, bot, update):
        text = "<b>Chicor</b> <i>v" + self.version + "</i>\n\n"\
            + "Flexible, plugin-based Telegram bot written in <b>Python</b> by @Ichicoro.\n"\
            + "<a href='https://github.com/Ichicoro/Chicor'>Fork me on GitHub!</a>"
        update.message.reply_text(text, parse_mode='HTML', disable_web_page_preview=True)


    # This method validates a config object (read from config.json)
    def __validate_and_load_config(self):
        try:
            self.updater = Updater(self.config['TELEGRAM_API_TOKEN'],
                                   user_sig_handler=self.__emergency_stop)
        except Exception:
            utils.pprint('Missing API token! Write it in the config.json file')
            return -1
        try:
            self.plugin_list = self.config['plugin_list']
        except Exception:
            utils.pprint('Missing plugin list. Set it up in the config.json file')
            return -1
        return 0


    def __enable_plugin(self, bot, update, args):
        if str(update.message.from_user.id) not in self.config['admin_list']:
            update.message.reply_text("You don't have enough privileges!")
            return

        if not len(args):
            update.message.reply_text("No plugin specified!")
            return

        if importlib.util.find_spec(args[0]) is not None:
            self.config['plugin_list'].append(args[0])
            update.message.reply_text("Plugin enabled. Restarting bot...")
            self.__restart()
        else:
            update.message.reply_text("Plugin not found.")


    def __disable_plugin(self, bot, update, args):
        if str(update.message.from_user.id) not in self.config['admin_list']:
            update.message.reply_text("You don't have enough privileges!")
            return

        if not len(args):
            update.message.reply_text("No plugin specified!")
            return

        if args[0] in self.config['plugin_list']:
            self.config['plugin_list'].remove(args[0])
            update.message.reply_text("Plugin disabled. Restarting bot...")
            self.__restart()
        else:
            update.message.reply_text("Plugin not found.")


    def __fix_plugin_config_settings(self):
        for plugin_name in self.plugin_list:
            if plugin_name not in self.config['plugin_settings']:
                for plugin in self.plugins:
                    if plugin.__class__.__name__ == plugin_name:
                        try:
                            self.config['plugin_settings'][plugin_name] = plugin.default_config
                        except Exception:
                            self.config['plugin_settings'][plugin_name] = {}
                        break


    def start(self):
        self.updater.start_polling()
        self.updater.idle()


    def __emergency_stop(self, signum = None, frame = None):
        self.stop()


    def stop(self, bot = None, update = None):
        if bot is not None and update is not None:
            if str(update.message.from_user.id) not in self.config['admin_list']:
                update.message.reply_text("You don't have enough privileges!")
                return
            update.message.reply_text("Stopping bot.")
            logging.info('stopping bot.')
        self.updater.stop()


    # RESTART BOT
    def __stop_and_restart(self):
        """Gracefully stop the Updater and replace the current process with a new one"""
        self.updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def __restart(self, bot = None, update = None):
        self.__save_config()
        if bot is not None and update is not None:
            bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
            if str(update.message.from_user.id) not in self.config['admin_list']:
                update.message.reply_text("You don't have enough privileges!")
                return
            update.message.reply_text('Bot is restarting...')
        Thread(target=self.__stop_and_restart).start()


    def __upgrade_config(self):
        if os.path.exists("config.json") and not os.path.exists("config.yaml"):
            import json
            logging.info('Converting config.json to config.yaml...')
            with open('config.json', 'r') as json_config:
                with open('config.yaml', 'w') as yaml_config:
                    yaml.dump(json.load(json_config), yaml_config)
            logging.info('Removing config.json...')
            os.remove('config.json')


    def __print_help(self, bot, update, args):
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
        help_text = ''
        if not len(args):
            help_text = '<b>Chicor</b> <i>v' + self.version + "</i>\n" \
            + "\nBuilt-in commands:" \
            + "\n<b>/help</b>: Prints this!" \
            + "\n<b>/info</b>: Prints information about the bot." \
            + "\n<b>/stop</b>: Stops the bot." \
            + "\n<b>/enable</b>: Enables plugins." \
            + "\n<b>/disable</b>: Disables plugins." \
            + "\n<b>/restart</b>: Restarts the bot.\n" \
            + "\nEnabled plugins:"
            for plugin in self.plugins:
                help_text += '\n<b>• ' + plugin.__class__.__name__ + '</b>'
                try:
                    help_text += ": " + plugin.description
                except AttributeError:
                    pass
        else:
            if args[0] in self.plugin_list:
                help_text = "<b>" + args[0] + "</b>"
                for plugin in self.plugins:
                    if plugin.__class__.__name__ == args[0]:
                        try:
                            help_text += ": " + plugin.description
                        except AttributeError:
                            help_text += ": No description available."
                        try:
                            help_text += "\n\n" + plugin.help_text
                        except AttributeError:
                            help_text += "\n\nNo help text available."
            else:
                help_text = "No such plugin exists."
        update.message.reply_text(help_text, parse_mode='HTML', disable_web_page_preview=True)


    def __setup(self):
        # Setup hardcoded handlers
        self.updater.dispatcher.add_handler(CommandHandler('stop', self.stop))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.__print_help, pass_args=True))
        self.updater.dispatcher.add_handler(CommandHandler('info', self.__print_info))
        self.updater.dispatcher.add_handler(CommandHandler('restart', self.__restart))
        self.updater.dispatcher.add_handler(CommandHandler('enable', self.__enable_plugin, pass_args=True))
        self.updater.dispatcher.add_handler(CommandHandler('disable', self.__disable_plugin, pass_args=True))

        # Add the plugins folder to the path list for module lookups
        sys.path.insert(0, './plugins')

        # Initialize plugins
        for plugin in self.plugin_list:
            logging.info(f'now loading: {plugin}')
            p = getattr(importlib.import_module(plugin, "plugins"), plugin)()
            self.plugins.append(p)

        # Fix any problem in the config settings
        self.__fix_plugin_config_settings()

        # Load each plugin's config from json to each instance
        for plugin in self.plugins:
            plugin.config = self.config['plugin_settings'][plugin.__class__.__name__]
            plugin.admin_list = self.config['admin_list']

        for plugin in self.plugins:
            try:
                plugin.on_load()
            except Exception:
                pass

        # Register message handler to self.__on_text
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.__on_text))


        # Register plugin handlers
        forbidden_commands = ["stop", "help", "enable", "disable", "info", "restart"]
        for plugin in self.plugins:
            for command, function in plugin.commands.items():
                # print(command, function)
                if command not in forbidden_commands:
                    self.updater.dispatcher.add_handler(
                        CommandHandler(command, function, pass_args=True))

        # Save settings to disk
        self.__save_config()

        # self.save_timer = self.__save_plugin_config()
        self.updater.job_queue.run_repeating(self.__save_plugin_config, interval=50, first=5)


    def __on_text(self, bot, update):
        for plugin in self.plugins:
            try:
                logging.info(f"calling on_text for: {plugin}")
                plugin.on_text(bot, update)
            except Exception:
                logging.warn(f'Plugin {plugin} has no on_text')
        logging.debug('finished execution of __on_text')




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                        format='%(name)s - %(levelname)s - %(message)s')
    bot = Bot()
    bot.start()
    bot.stop()
