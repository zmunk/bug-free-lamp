"""
in terminal: python -i multi_browser.py -u [url]
make sure to specify k-1 sessions if k is the desired number
then, open a session manually
in terminal: quit()
"""

import sys
import argparse
import selenium
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from getpass import getpass

DRIVER_LOC = "chromedriver80.exe"
DEFAULT_URL = 'https://lms.sehir.edu.tr/mod/adobeconnect/view.php?id=64596'


def parse_args():
    ''' parse arguments from command line '''

    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-u", "--url", help="url", type=str, default=None)

    # Parse arguments
    args = parser.parse_args()

    return args


class Session(Thread):
    def __init__(self, username, password, url=None):
        Thread.__init__(self)
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(DRIVER_LOC)
        if url:
            self.url = url
        else:
            self.url = DEFAULT_URL


    def run(self):
        self.browser.get(self.url)
        try:
            mysehir = self.browser.find_element_by_xpath("//div[@class='potentialidp']/a")
            mysehir.click()
        except selenium.common.exceptions.NoSuchElementException:
            pass

        username_field = self.browser.find_element_by_name("UserName")
        password_field = self.browser.find_element_by_name("Password")

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        self.browser.find_element_by_id("submitButton").click()

        join_meeting_btn = self.browser.find_element_by_id('kati2')
        join_meeting_btn.click()

        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
        self.browser.switch_to.window(self.browser.window_handles[-1])

        self.browser.find_element_by_tag_name('a').click()
        try: 
            kayitli_btn = self.browser.find_element_by_id('registeredTab')
        except selenium.common.exceptions.NoSuchElementException:
            self.browser.find_element_by_tag_name('a').click()
            kayitli_btn = self.browser.find_element_by_id('registeredTab')
        kayitli_btn.click()

        # login in second time
        username_field = self.browser.find_element_by_name('login')
        password_field = self.browser.find_element_by_name('password')
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        self.browser.find_element_by_id('login-button').click()

        # open in browser
        browser_btn = self.browser.find_element_by_class_name('open-in-browser-button')
        self.browser.execute_script("arguments[0].click();", browser_btn)



if __name__ == '__main__':
    args = parse_args()
    username = input("Username: ")
    password = getpass()
    n = int(input("number of sessions: "))
    sessions = []
    for i in range(n):
         sessions.append(Session(username, password, url=args.url).start())