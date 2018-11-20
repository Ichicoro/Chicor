from utils import get_admin_ids

class settitle():
    def __init__(self):
        self.commands = {
            'settitle': self.titlesetter
        }
        self.description = "Title-setting, man."
        self.help_text = "Write /settitle &lt;title&gt; to set the chat title! <i>Admin only</i>"


    def titlesetter(self, bot, update, args):
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')

        if update.message.from_user.id not in get_admin_ids(bot, update.message.chat_id)+self.admin_list:
            update.message.reply_text("You don't have enough privileges!")
            return

        update.message.reply_text("I'm still a work-in-progress.")


