from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
import selenium
from credentials import USERNAME, PASSWORD

browser = webdriver.Chrome("driver/chromedriver80.exe")

url = 'https://lms.sehir.edu.tr/mod/adobeconnect/view.php?id=64596'
browser.get(url)

mysehir = browser.find_element_by_xpath("//div[@class='potentialidp']/a")
mysehir.click()

username_field = browser.find_element_by_name("UserName")
password_field = browser.find_element_by_name("Password")

username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)

browser.find_element_by_id("submitButton").click()

# MAIN PAGE REACHED

main_window = browser.window_handles[0]
join_meeting_btn = browser.find_element_by_id('kati2')
join_meeting_btn.click()

WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
browser.switch_to.window(browser.window_handles[-1])

# todo: fix
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
username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)
browser.find_element_by_id('login-button').click()

app_btn = browser.find_element_by_class_name('open-in-app-button')
browser.execute_script("arguments[0].click();", app_btn)

## todo: fix
actions = ActionChains(browser)
actions.send_keys(Keys.LEFT)
actions.send_keys(Keys.ENTER)
actions.perform()




