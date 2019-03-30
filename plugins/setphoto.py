import utils
import os

class setphoto():
    def __init__(self):
        self.config = {}
        self.commands = {
            'setphoto': self.photosetter
        }
        self.default_config = {
            'require_admin_privileges': True
        }
        self.description = "Photo-setting, man."
        self.help_text = "Write /setphoto on a photo to set it as the chat photo! <i>Admin only</i>"


    def photosetter(self, bot, update, args):
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')

        target_message = update.message.reply_to_message

        if target_message is None:
            update.message.reply_text("You haven't replied to a message!")
            return

        if len(target_message.photo) == 0:
            update.message.reply_text("The message you replied to doesn't contain a photo!")
            return

        if self.config['require_admin_privileges'] and not is_chat_admin(bot, update.message.chat_id):
            update.message.reply_text("You don't have enough privileges!")
            return

        print(target_message.photo)
        photo_file = target_message.photo[len(target_message.photo)-1].get_file().download()

        bot.setChatPhoto(chat_id=update.message.chat_id, photo=open(photo_file, 'rb'))

        os.remove(photo_file)
