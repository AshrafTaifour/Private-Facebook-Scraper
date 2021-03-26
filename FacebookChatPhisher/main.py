from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as soup
import time
from lxml import html  # to parse html
from tbselenium.tbdriver import TorBrowserDriver
import os


def getFriendsListHTMLPage(driver, uname):
    yourFriendlistPage = getFriendsListPage(uname)

    driver.get(yourFriendlistPage)

    # scroll 10 times to get all friends on page
    for j in range(0, 10):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # get full HTML page of friends
    return driver.page_source


def loginToFacebook(exePath, useremail, userpass):
    # store original path of the directory (tor is changing the path when executing)
    originalPath = os.getcwd()
    if('chrome' in exePath):
        # will turn off notification for FB to allow webscraping for windows
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(exePath, options=chrome_options)
        # will open the webpage
        driver.get("http://www.facebook.com")
    elif('tor' in exePath):
        # for linux, uses tor browser.
        driver = TorBrowserDriver(exePath)
        # will open the webpage
        driver.get("https://www.facebookcorewwwi.onion/")
    else:
        print(f"'tor' or 'chrome' are not in your path's name, please change the name of your chrome driver to include the word chrome in it or the tor directory to include the word tor.")
        return

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
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()
    # change directory back to the original so we can save friendsURLs page and likePages in the same directory as the project.
    os.chdir(originalPath)

    return driver

# will return the URL of the user's friends list page based on whether they have a user name or not


def getFriendsListPage(uname):
    # if account has no real username
    retStr = ""
    if 'profile.php?' in uname:
        retStr = f'https://www.facebookcorewwwi.onion/{uname}&sk=friends'
    else:
        retStr = f"https://www.facebook.com/{uname}/friends_all"

    return retStr


# will parse pagesource and return a list of HREFs, parses through friends list page and a friend's likes page
def parseHTML(HTMLPAGE, typeOfPage: str, friendNumber: int):
    # use beautifulsoup to parse HTML
    page_soup = soup(HTMLPAGE, "html.parser")
    hrefs = None

    # obtain your friends' URLs from the full source page HTML
    if(typeOfPage == "friendsurls"):
        # oajrlxb2 class contains many URLS that will be useful for finding friends' page URLs
        containers = page_soup.findAll("a", {"class": "oajrlxb2"})

        # save the page to local storage for local parsing
        with open("friendListPage.html", "w", encoding='utf-8') as file:
            file.write(str(containers))
        # lxml.html requires an actual html page to be passed so saving locally is required.
        tree = html.parse("friendListPage.html")
        html.tostring(tree)
        hrefs = tree.xpath('//@href')
        # will parse hrefs, take only friends' pages and append all_likes to them so we can access their likes.
        hrefs = parseURLS(hrefs)

    # obtain a friend's likes
    elif(typeOfPage == "friendslikes"):
        # d2edcug0 span contains the name of the liked page
        containers = page_soup.findAll("span", {"class": "d2edcug0"})

        # save the page to local storage for local parsing
        with open(f"friendLikesPage{friendNumber}.html", "w", encoding='utf-8') as file:
            file.write(str(containers))

    else:
        print("INVALID INPUT")

    return hrefs


# parses through the list of URLS
def parseURLS(lst: list) -> list:
    newLst = []
    for link in lst:
        # links that contain 'friends_mutual' in it include your friend's URLs, this is a good way to only select for friendsURLs...
        # and discard any extra URLs.
        if"friends_mutual" in link:
            size = len(link)
            modString = link[:size - 14]
            newLst.append(modString)
    return newLst


def scrapeLikePages(driver, friendURLs, numOfFriends):
    i = 0
    while(i < numOfFriends and i < len(friendURLs)):
        friendLikesPage = friendURLs[i] + "likes_all"
        driver.get(friendLikesPage)
        time.sleep(3)
        # scroll to get the entire 'likes' page
        for k in range(10):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        likesPage = driver.page_source
        parseHTML(likesPage, "friendslikes", i)
        i += 1


if __name__ == '__main__':
    # import sensitive information if running locally 
    from secretDirectory import secret

    email = secret.EMAIL
    uname = secret.UNAME
    passw = secret.passw
    numOfFriendsToScrape = 2

    # login, visit the facebook page and return the driver

    # Windows Scraping
    # windowsPath = secret.windowsPath

    # Linux Scraping
    linuxPath = secret.linuxPath

    driver = loginToFacebook(linuxPath, email, passw)
    time.sleep(8)

    FULLHTMLPAGE = getFriendsListHTMLPage(driver, uname)

    # will parse the HTML page to obtain hrefs of friends.
    friendURLS = parseHTML(FULLHTMLPAGE, "friendsurls", 1)

    scrapeLikePages(driver, friendURLS, numOfFriendsToScrape)
