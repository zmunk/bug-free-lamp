"""
type "python adobe_connect_hack.py -h" in terminal to see options
"""

import sys
import argparse
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from getpass import getpass
# from credentials import USERNAME, PASSWORD

def parse_args():
    ''' parse arguments from command line '''

    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-u", "--url", help="url", type=str, default=None)
    parser.add_argument("-a", "--app", help="launch in app (default: browser)", action="store_true")
    parser.add_argument("-d", "--driver", help="driver location", default=None)

    # Parse arguments
    args = parser.parse_args()

    return args

def get_browser(driver_loc):
    browser = webdriver.Chrome(driver_loc)
    return browser

def hack(browser, url, in_app, username, password):
    ''' automatically open adobe connect class
    url: url of meeting page on lms
    in_app (boolean): open in app if true, otherwise open in browser
    '''

    # default url
    if not url:
        url = 'https://lms.sehir.edu.tr/mod/adobeconnect/view.php?id=64596'


    browser.get(url)
    try:
        mysehir = browser.find_element_by_xpath("//div[@class='potentialidp']/a")
        mysehir.click()
    except selenium.common.exceptions.NoSuchElementException:
        pass

    username_field = browser.find_element_by_name("UserName")
    password_field = browser.find_element_by_name("Password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    browser.find_element_by_id("submitButton").click()

    # MAIN PAGE REACHED

    main_window = browser.window_handles[0]
    join_meeting_btn = browser.find_element_by_id('kati2')
    join_meeting_btn.click()

    WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
    browser.switch_to.window(browser.window_handles[-1])

    browser.find_element_by_tag_name('a').click()
    try: 
        kayitli_btn = browser.find_element_by_id('registeredTab')
    except selenium.common.exceptions.NoSuchElementException:
        browser.find_element_by_tag_name('a').click()
        kayitli_btn = browser.find_element_by_id('registeredTab')
    kayitli_btn.click()

    # login in second time
    username_field = browser.find_element_by_name('login')
    password_field = browser.find_element_by_name('password')
    username_field.send_keys(username)
    password_field.send_keys(password)
    browser.find_element_by_id('login-button').click()

    if in_app:
        # open in app
        app_btn = browser.find_element_by_class_name('open-in-app-button')
        browser.execute_script("arguments[0].click();", app_btn)

        ## todo: fix
        actions = ActionChains(browser)
        actions.send_keys(Keys.LEFT)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    else:
        # open in browser
        browser_btn = browser.find_element_by_class_name('open-in-browser-button')
        browser.execute_script("arguments[0].click();", browser_btn)

def main():
    args = parse_args()
    if args.driver:
        driver_loc = args.driver
    else:
        driver_loc = "chromedriver80.exe"

    username = input("Username: ")
    password = getpass()

    browser = get_browser(driver_loc)
    hack(browser, args.url, args.app, username, password)

    

if __name__ == '__main__':
    main()




