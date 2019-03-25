import urllib.parse, re, requests


class rule34():
    def __init__(self):
        self.commands = {
            'rule34': self.search34
        }
        self.description = "If it exists, there's porn of it."
        self.help_text = "Write /rule34 &lt;search query&gt; to search for... stuff."


    def search34(self, bot, update, args):
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
        if not len(args):
            update.message.reply_text(text="No search terms sent", quote=True)
            return

        query = '+'.join(args)
        tags = urllib.parse.quote(query, safe='~()*!.\'').replace('%2B', '+')
        req = requests.get(f"https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1&tags={tags}")
        data = req.text
        imgurlarr = re.findall(r'file_url="(?:https?:)?(\/\/img\.rule34\.xxx\/images\/\d+\/[0-9a-f]+\.\w+)"', data, re.I)

        if imgurlarr is None or len(imgurlarr) == 0:
            update.message.reply_text(text="No results found", quote=True)
        else:
            update.message.reply_photo(photo=f"https:{imgurlarr[0]}", quote=True)
