# Pretty-prints a string with equal signs
def pprint(s):
    print(f"{len(s)}\n{s}\n{len(s)}")


def generate_config_file():
    sample_settings = {
        "TELEGRAM_API_TOKEN": "",
        "plugin_list": [ "hello_plugin" ],
        "plugin_settings": [
            {
                "plugin_name":
            }
        ]
    }
    with open('config.json', 'w') as file:
        json.dump(sample_settings, file)
