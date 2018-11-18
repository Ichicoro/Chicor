class hello_plugin():
    def __init__(self):
        self.commands = {
            'hello': self.hello
        }
        

    def test(self):
        print('hello_plugin works fine!')


    def hello(self, bot, update):
        update.message.reply_text(f'Hi {update.message.from_user.username}!')
        # print('hey gay')
        # self.pizza += 1
        # print(f'pizzas: {self.pizza}')


    def on_text(self, bot, update):
        if 'hello' in update.message.text:
            update.message.reply_text(f"Hi! Echo: {update.message.text}")
        # bot.send_message(chat_id=update.message.chat_id, text=f"Hi! Echo: {update.message.text}")

