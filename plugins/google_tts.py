from gtts import gTTS, gTTSError, lang
import telegram, os
from io import BytesIO


class google_tts():
    def __init__(self):
        self.config = {}
        self.commands = {
            'say': self.say_handler,
            'languages': self.print_supported_languages
        }
        self.default_config = {}    # If this exists, it's copied to the plugin config in config.yaml (Not required)
        self.description = "Plugin description"
        self.help_text = "Plugin help text"


    def on_load(self):
        pass


    def say_handler(self, bot, update, args):
        # if not len(args):
        #     update.message.reply_text("This command requires arguments")
        #     return
        # elif len(args) == 1:
        #     update.message.reply_text("Please :)")
        #     return
        completed_msg = ""
        for arg in range(1, len(args)):
            print(arg)
            completed_msg += args[arg] + " "
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.RECORD_AUDIO)
        
        tts_fp = BytesIO()
        try:
            tts_audio = gTTS(completed_msg, lang=args[0])
        except gTTSError:
            gtts.gTTSError.infer_msg(tts_audio)
            return
        # tts_audio.write_to_fp(tts_fp)
        tts_audio.save("test.mp3")
        # print(tts_fp.read())
        # print(f.read())
        update.message.reply_voice(voice=open("test.mp3", 'rb'))
        os.remove('test.mp3')
        


    def print_supported_languages(self, bot, update, args):
        langs = lang.tts_langs()
        msg = "<b>Supported Languages:</b>"
        for (langkey, langname) in langs.items():
            msg += f"\n- <b> {langname}:</b> {langkey}"
        update.message.reply_text(msg, parse_mode='HTML')
