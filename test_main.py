import time
import codecs
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as soup
from lxml import html  # to parse html
from unittest import TestCase
from tbselenium.tbdriver import TorBrowserDriver
#import our file that has user login and the path to the tor and chrome drivers
from secretDirectory import secret
from main import parseHTML, parseURLS

class Test(TestCase):
    #uncomment this test if on Windows
    #to ensure the libraries are working.
    def test_windowsLogin(self, path = secret.windowsPath, email = secret.EMAIL, passw = secret.passw):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(path, options=chrome_options)
        driver.get("http://www.facebook.com")
        usernameBox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        passwordBox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

        usernameBox.clear()
        usernameBox.send_keys(email)
        passwordBox.clear()
        passwordBox.send_keys(passw)

        button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

        time.sleep(5)
        #assert if you're now on the homepage or if an 'incorrect password' error was thrown which would have a different URL
        assert(driver.current_url == 'https://www.facebook.com/')

    #uncomment this test if on linux
    #check the README to ensure geckodriver is setup properly for this and that tor is installed using 'sudo apt install tor' for tbselenium
    #visit https://github.com/webfp/tor-browser-selenium for more information
    # def test_linuxLogin(self, path = secret.linuxPath, email = secret.EMAIL, passw = secret.passw):
    #     # for linux, uses tor browser.
    #     driver = TorBrowserDriver(path)
    #
    #     driver.get("http://www.facebook.com")
    #     usernameBox = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    #     passwordBox = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    #
    #     usernameBox.clear()
    #     usernameBox.send_keys(email)
    #     passwordBox.clear()
    #     passwordBox.send_keys(passw)
    #
    #     button = WebDriverWait(driver, 2).until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    #
    #     time.sleep(5)
    #     # assert if you're now on the homepage or if an 'incorrect password' error was thrown which would have a different URL
    #     assert (driver.current_url == 'https://www.facebook.com/')


    #please setup secret.testFriendsURLsPage to a the downloaded HTML source of your own "friends list" page that shows all your friends on Facebook
    #here we are testing ParseHTMLs ability to parse full source HTML page and it returning hrefs that can be used to find friendsURLs
    def test_parse_html_friendsURLs(self, type_of_page="friendsurls", friendNumber=None):
        #TODO: find a way to read an HTML file that can be passed to the parseHTML function.
        #TODO: parseHTML function accepted driver.page_source from selenium so it has to be in a similar format to that.
        #TODO: currently broken
        with codecs.open("testURLsPage.html", "r", 'utf-8') as friendsURLsPage:
            pass
        print(friendsURLsPage)
        result = True
        allHrefs = parseHTML(friendsURLsPage, type_of_page, friendNumber)
        for link in allHrefs:
            print(link)
            if 'https://www.facebook.com/' not in link:
                result = False

        assert(result)


