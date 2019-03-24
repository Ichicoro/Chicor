import threading, json, yaml


# Pretty-prints a string with equal signs
def pprint(s):
    print(f"{'='*len(s)}\n{s}\n{'='*len(s)}")


def generate_config_file():
    sample_settings = {
        "TELEGRAM_API_TOKEN": "",
        "plugin_list": [ "hello_plugin", "rule34", "lyrics" ],
        "admin_list": [],
        "plugin_settings": []
    }
    with open('config.yaml', 'w') as file:
        yaml.dump(sample_settings, file)


def set_interval(interval, times = -1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()

            # This is another function to be executed
            # in a different thread to simulate setInterval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap


def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
