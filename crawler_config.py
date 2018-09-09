from selenium import webdriver

def initCrawler():
    # ----------These are headless options-----------------
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    # Change Headless User-Agent to general User-Agent.
    TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    return webdriver.Chrome("./chromedriver", chrome_options=options)

    # -------------------------------------------------------
