import os
import time
import codecs
import unittest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as soup
from lxml import html  # to parse html
from tbselenium.tbdriver import TorBrowserDriver
import sys
# super hacky fix to get parent directory by adding it to PATH
sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + '/..')
from main import loginToFacebook, scrapeLikePages
from friendListRetriever import getFriendsListPage
from htmlParsers import parseFriendsPage, parseLikesPage, parseURLS
from driver import * 
from secretDirectory import secret

'''NOTE: behavior is different for terminal execution and VSCODE execution; 
VSCODE runs tests from ~/Desktop/4990/fbscrapeandlogin/fbLoginAndScrape/FacebookChatPhisher$ directory
while Terminal will run tests from ~/Desktop/4990/fbscrapeandlogin/fbLoginAndScrape/FacebookChatPhisher/Tests$ directory
this means that whenever we use codecs.open() for onionTestfiles an error may be raised based on which program executes the program
'''
#Tests that should work on the clear-net browser (anything but Tor)
class ClearNetTest(unittest.TestCase):
    def setUp(self):
        driver_path=secret.exePath
        email=secret.EMAIL
        passw=secret.passw
        browser_mode = guessBrowserFromPath(driver_path)
        self.driver = getDriver(driver_path, browser_mode )
        loginToFacebook(self.driver, email, passw)
    
    def tearDown(self):
        self.driver.quit()

    # test the drivers for Facebook using day to day drivers
    # would ideally create separate test for each browser except nobody has all the supported browsers
    def test_driver(self):
        assert('https://www.facebook.com/' in self.driver.current_url)

    # testing the function that gets friends list url
    def test_getFriendsListPage(self, uname=secret.UNAME):
        website="https://www.facebook.com"
        yourFriendlistPage = getFriendsListPage(uname, website)
        assert(f"{website}/{uname}&sk=friends" in yourFriendlistPage or
               f"{website}/{uname}/friends_all" in yourFriendlistPage
               )

# Tests that should work on Tor browser
class DarkWebTest(unittest.TestCase):
    def setUp(self):
        driver_path=secret.exePath
        email=secret.EMAIL
        passw=secret.passw
        tor_path= secret.torBrowserPath
        self.driver = getDriver(driver_path, Browser.TOR, tor_path)
        loginToFacebook(self.driver, email, passw)

    def tearDown(self):
        self.driver.quit()
    # make sure TOR driver atleast opened page
    def test_driver(self):
        assert ('https://www.facebookcorewwwi.onion/' in self.driver.current_url)

    # testing the function that gets friends list url
    def test_getFriendsListPage(self, uname=secret.UNAME):
        website="https://www.facebookcorewwwi.onion"
        yourFriendlistPage = getFriendsListPage(uname, website)
        assert(f"{website}/{uname}&sk=friends" in yourFriendlistPage or
                f"{website}/{uname}/friends_all" in yourFriendlistPage
               )

    #will login and scrape the likes pages of the friends in this list and then save those like pages locally, this will check 
    def test_scrapeLikePages(self, numFriendstoScrape = 2):
        friendURLs = ['https://www.facebookcorewwwi.onion/abdullah.arif115/', 'https://www.facebookcorewwwi.onion/ashraf.tayfour/']
        scrapeLikePages(self.driver, friendURLs, numFriendstoScrape, os.getcwd())
        result = True

        try:
            with codecs.open("friendLikesPage0.html") as f:
                pass
        except IOError:
            result &= False

        try:
            with codecs.open("friendLikesPage1.html") as f:
                pass
        except IOError:
            result &= False
        # Ensure both friends page exist 
        assert(result)
    

class HTMLProcessingTest(unittest.TestCase):
    # please setup secret.testFriendsURLsPage to a the downloaded HTML source of your own "friends list" page that shows all your friends on Facebook
    # here we are testing ParseHTMLs ability to parse full source HTML page and it returning hrefs that can be used to find friendsURLs
    def test_parse_html_friendsURLs(self):
        with codecs.open("testURLsPageOnion.html", "r", 'utf-8') as friendsURLsPage:
            result = True
            allHrefs = parseFriendsPage(friendsURLsPage)
            for link in allHrefs:
                if 'https://www.facebook.com/' not in link and 'https://www.facebookcorewwwi.onion/' not in link:
                    print(result)
                    result = False

        assert(result)

    def test_parse_html_friendsLikes(self, friendNumber=7357):
        # 7357 means test, this testfunction will take in raw HTML of likesPage and should output an html file named friendLikesPage7357.html that will include the
        # names of the liked pages and the interest category of that liked page
        with codecs.open("testLikesPage1Onion.html", "r", 'utf-8') as friendsLikesPage:
            result = True
            parseLikesPage(friendsLikesPage, friendNumber, os.getcwd())

        try:
            with codecs.open("friendLikesPage7357.html") as f:
                pass
        except IOError:
            result = False

        assert(result)

    #takes links that have friends_mutual in it and replaces it with the link to their page
    def test_parseURLs(self):
        givenList = ['https://www.facebook.com/profile.php?id=100008186476906', 'https://www.facebook.com/ashraf.tayfour/friends_mutual', 'https://www.facebook.com/abdullah.arif115/friends_mutual', 'https://www.facebook.com/profile.php?id=100064037088173' ,'https://www.facebook.com/profile.php?id=100064037088173/friends_mutual']
        expectedReturn = ['https://www.facebook.com/ashraf.tayfour/', 'https://www.facebook.com/abdullah.arif115/', 'https://www.facebook.com/profile.php?id=100064037088173/']

        actualReturn = parseURLS(givenList)

        self.assertCountEqual(expectedReturn, actualReturn)

if __name__ == '__main__':
    unittest.main()


