from selenium import webdriver


def init_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    return webdriver.Chrome(executable_path='./settings/chromedriver',
                            chrome_options=chrome_options
                            )
