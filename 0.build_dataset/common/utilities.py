from selenium import webdriver


def init_browser(watch=False):
    chrome_options = webdriver.ChromeOptions()
    if not watch:
        chrome_options.add_argument('headless')
    return webdriver.Chrome(executable_path='./settings/chromedriver',
                            chrome_options=chrome_options
                            )
