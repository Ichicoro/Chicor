class hello_plugin():
    def __init__(self):
        self.commands = {
            'hello': self.hello
        }
        self.default_settings = {
            'test_key': "working fine here!"
        }


    def test(self):
        print('hello_plugin works fine!')


    def hello(self, bot, update):
        update.message.reply_text(f'Hi {update.message.from_user.username}!')


    def on_text(self, bot, update):
        if 'hello' in update.message.text:
            update.message.reply_text(f"Hi! Echo: {update.message.text}")
