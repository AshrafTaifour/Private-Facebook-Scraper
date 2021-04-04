from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from friendListRetriever import getFriendsListHTMLPage
from seleniumUtil import scrollToBottomOfPage
from htmlParsers import parseFriendsPage, parseLikesPage

def loginToFacebook(driver, useremail: str, userpass: str):
    # targets username and password boxes
    usernameBox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    passwordBox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # enters username and password
    usernameBox.clear()
    usernameBox.send_keys(useremail)
    passwordBox.clear()
    passwordBox.send_keys(userpass)

    # login button is targeted and clicked
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()


def scrapeLikePages(driver, friendURLs: list, maxFriends : int, outputPath: str):
    numFriends = min(maxFriends, len(friendURLs))
    for i in range(numFriends):
        friendLikesPage = friendURLs[i] + "likes_all"
        driver.get(friendLikesPage)
        time.sleep(3)
        scrollToBottomOfPage(driver, 10)
        likesPage = driver.page_source
        parseLikesPage(likesPage, i, outputPath)


if __name__ == '__main__':
    # import sensitive information if running locally 
    from secretDirectory import secret
    # also get driver file to use 
    from driver import getDriver, Browser
    from os import getcwd
    email=secret.EMAIL
    passw=secret.passw
    uname = secret.UNAME
    tor_path=secret.torBrowserPath
    driver_path=secret.exePath
    numOfFriendsToScrape = 2
    driver = getDriver(driver_path, Browser.FIREFOX, tor_path)

    loginToFacebook(driver, email, passw)
    time.sleep(8)

    FULLHTMLPAGE = getFriendsListHTMLPage(driver, uname)

    # will parse the HTML page to obtain hrefs of friends.
    friendURLS = parseFriendsPage(FULLHTMLPAGE)
    print(friendURLS)
    print(len(friendURLS))
    scrapeLikePages(driver, friendURLS, numOfFriendsToScrape, getcwd())

    driver.close()