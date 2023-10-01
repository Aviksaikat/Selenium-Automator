# Selenium Automator

- This is a class tempalte for creating python selenium bots for downaloding images


# Usage

```py


def main():
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]

    urls = ["https://google.com"]

    driver_path = r"~/chromedriver"
    path_to_save = (
        r"~/SeleniumBotPython/media"
    )

    bot = SeleniumBot(username, password, driver_path, path_to_save)

    driver = bot.setupDriver()
    if driver:
        print(f"{bot.green}[*]Driver setup successful{bot.reset}")
    else:
        print(f"{bot.red}[!]Driver setup unsuccessful{bot.reset}")
        exit(-2)

    # Let your imaginaton do the rest ;)
    
if __name__ == "__main__":
    main()
```