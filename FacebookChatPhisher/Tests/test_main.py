
import os
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
import sys
# hacky fix to get parent directory
sys.path.append(os.getcwd() + '/..')
from main import loginToFacebook, getFriendsListPage, parseHTML, parseURLS, scrapeLikePages
from secretDirectory import secret

# import our file that has user login and the path to the tor and chrome drivers


class Test(TestCase):
    #originalPath = os.getcwd()

    # store original path of the directory (tor is changing the path when executing)

    # uncomment this test if on Windows
    # to ensure the libraries are working.
    def test_windowsLogin(self, path=secret.windowsPath, email=secret.EMAIL, passw=secret.passw):
        # for windows, uses chrome browser.
        driver = loginToFacebook(path, email, passw)

        # assert if you're now on the homepage or if an 'incorrect password' error was thrown which would have a different URL
        assert('https://www.facebook.com/' in driver.current_url)

    # uncomment this test if on linux
    # check the README to ensure geckodriver is setup properly for this and that tor is installed using 'sudo apt install tor' for tbselenium
    # visit https://github.com/webfp/tor-browser-selenium for more information
    def test_linuxLogin(self, path=secret.linuxPath, email=secret.EMAIL, passw=secret.passw):
        # for linux, uses tor browser.
        driver = loginToFacebook(path, email, passw)
        # assert if you're now on the homepage or if an 'incorrect password' error was thrown which would have a different URL
        assert ('https://www.facebookcorewwwi.onion/' in driver.current_url)

    # please setup secret.testFriendsURLsPage to a the downloaded HTML source of your own "friends list" page that shows all your friends on Facebook
    # here we are testing ParseHTMLs ability to parse full source HTML page and it returning hrefs that can be used to find friendsURLs

    def test_parse_html_friendsURLs(self, type_of_page="friendsurls", friendNumber=None):
        # change directory back to the original so we can save friendsURLs page and likePages in the same directory as the project.
        # os.chdir(Test.originalPath)
        with codecs.open("testURLsPageOnion.html", "r", 'utf-8') as friendsURLsPage:
            result = True
            allHrefs = parseHTML(friendsURLsPage, type_of_page, friendNumber)
            for link in allHrefs:
                if 'https://www.facebook.com/' not in link and 'https://www.facebookcorewwwi.onion/' not in link:
                    print(result)
                    result = False

        assert(result)

    def test_parse_html_friendsLikes(self, type_of_page="friendslikes", friendNumber=7357):
        # 7357 means test, this testfunction will take in raw HTML of likesPage and should output an html file named friendLikesPage7357.html that will include the
        # names of the liked pages and the interest category of that liked page
        with codecs.open("testLikesPage1Onion.html", "r", 'utf-8') as friendsLikesPage:
            result = True
            parseHTML(friendsLikesPage, type_of_page, friendNumber)

        try:
            with codecs.open("friendLikesPage7357.html") as f:
                pass
        except IOError:
            result = False

        assert(result)

    # testing the function that gets friends list url
    def test_getFriendsListPage(self, path=secret.linuxPath, email=secret.EMAIL, passw=secret.passw, uname=secret.UNAME):
        driver = loginToFacebook(path, email, passw)
        yourFriendlistPage = getFriendsListPage(uname)

        assert(
            f"https://www.facebook.com/{uname}/friends_all" in yourFriendlistPage or f"https://www.facebookcorewwwi.onion/{uname}&sk=friends" in yourFriendlistPage)

    #takes links that have friends_mutual in it and replaces it with the link to their page
    def test_parseURLs(self):
        givenList = ['https://www.facebook.com/profile.php?id=100008186476906', 'https://www.facebook.com/ashraf.tayfour/friends_mutual', 'https://www.facebook.com/abdullah.arif115/friends_mutual', 'https://www.facebook.com/profile.php?id=100064037088173' ,'https://www.facebook.com/profile.php?id=100064037088173/friends_mutual']
        expectedReturn = ['https://www.facebook.com/ashraf.tayfour/', 'https://www.facebook.com/abdullah.arif115/', 'https://www.facebook.com/profile.php?id=100064037088173/']

        actualReturn = parseURLS(givenList)


        self.assertCountEqual(expectedReturn, actualReturn)

    #will login and scrape the likes pages of the friends in this list and then save those like pages locally, this will check 
    def test_scrapeLikePages(self, path=secret.linuxPath, email=secret.EMAIL, passw=secret.passw, numFriendstoScrape = 2):
        driver = loginToFacebook(path, email, passw)
        friendURLs = ['https://www.facebookcorewwwi.onion/abdullah.arif115/', 'https://www.facebookcorewwwi.onion/ashraf.tayfour/']
        scrapeLikePages(driver, friendURLs, numFriendstoScrape)

        result = True

        try:
            with codecs.open("friendLikesPage0.html") as f:
                pass
        except IOError:
            result = False

        try:
            with codecs.open("friendLikesPage1.html") as f:
                pass
        except IOError:
            result = False

        assert(result)




