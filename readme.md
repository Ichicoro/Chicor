# Chicor

Flexible, plugin-based Telegram bot written in **Python**.

## How to setup
Clone the repo, install the modules and doop doop.

## How to write plugins for the bot
### Basic structure
```python
class plugin_name():
    '''
    The plugin name must be the same as the filename of the module
    Plugins are also able to access the following variables:
    - self.admin_list   -> the admin_list defined in config.json
    '''

    def __init__(self):
        self.config = {}
        self.commands = {
            'command1': handler1,
            'command2': handler2
        }
        self.default_config = {} # If this exists and it contains a dict, it's copied to the plugin config in config.json (Not required)
        self.description = "Plugin description"
        self.help_text = "Plugin help text"


    def handler1(self, bot, update, args):
        update.message.reply_text("Hello?")


    def handler1(self, bot, update, args):
        update.message.reply_text("Hello!")


    def on_text(self, bot, update):
        update.message.reply_text("I get called when a message gets sent")

    # There are also other handlers for other types of messages.
```

After writing the plugin, either enable it with `/enable <plugin_name>` or by manually adding the plugin name in the `config.json`
