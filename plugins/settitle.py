import utils


class settitle():
    def __init__(self):
        self.config = {}
        self.commands = {
            'settitle': self.titlesetter
        }
        self.default_config = {
            'require_admin_privileges': True
        }
        self.description = "Title-setting, man."
        self.help_text = "Write /settitle &lt;title&gt; to set the chat title! <i>Admin only</i>"


    def titlesetter(self, bot, update, args):
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')

        if self.config['require_admin_privileges'] and not utils.is_chat_admin(bot, update.message.chat_id):
            update.message.reply_text("You don't have enough privileges!")
            return

        bot.setChatTitle(chat_id=update.message.chat_id, title=" ".join(args))
