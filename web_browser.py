from selenium import webdriver


def openbrowser():

    browser = webdriver.Chrome()
    browser.get('https://www.baidu.com')

    cookie = {'name': 'H_PS_PSSID',
              'value': '32818_1433_32874_32723_32231_7516_7605_32117_26350_32914; path=/; domain=.baidu.com'}
    browser.add_cookie(cookie)

    print(browser.page_source)
    browser.close()