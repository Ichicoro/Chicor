import threading

# Pretty-prints a string with equal signs
def pprint(s):
    print(f"{len(s)}\n{s}\n{len(s)}")


def generate_config_file():
    sample_settings = {
        "TELEGRAM_API_TOKEN": "",
        "plugin_list": [ "hello_plugin" ],
        "plugin_settings": []
    }
    with open('config.json', 'w') as file:
        json.dump(sample_settings, file, indent=4, sort_keys=True)


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
