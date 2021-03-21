from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as soup
import time
from lxml import html  # to parse html
from secretDirectory import secret
from tbselenium.tbdriver import TorBrowserDriver
import os

#username is name in url


def getFriendsLikes(uname, email, passw, numFriendsToScrape, path):
    # will turn off notification for FB to allow webscraping for windows
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # store original path of the directory (tor is changing the path when executing)
    originalPath = os.getcwd()

    if('chrome' in path):
        driver = webdriver.Chrome(path, options=chrome_options)
        driver.get("http://www.facebook.com")
    elif('tor' in path):
        # for linux, uses tor browser.
        driver = TorBrowserDriver(path)
        driver.get("https://www.facebookcorewwwi.onion/")
    else:
        print(f"'tor' or 'chrome' are not in your path's name, please change the name of your chrome driver to include the word chrome in it or the tor directory to include the word tor.")
        return

    # will open the webpage

    # target username field
    usernameBox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    passwordBox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # enters username and password
    usernameBox.clear()
    usernameBox.send_keys(email)
    passwordBox.clear()
    passwordBox.send_keys(passw)

    # login button is targeted and clicked
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    #
    time.sleep(8)
    #facebookURL = driver.current_url

    # if account has no real username
    if 'profile.php?' in uname:
        print('************************************************************')
        driver.get(f'https://www.facebookcorewwwi.onion/{uname}&sk=friends')
        print('**************************************************************')
    else:
        driver.get(f"https://www.facebook.com/{uname}/friends_all")

    # scroll 10 times to get all friends on page
    for j in range(0, 10):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # get full HTML page of friends
    FULLHTMLPAGE = driver.page_source

    # change directory back to the original so we can save friendsURLs page and likePages in the same directory as the project.
    os.chdir(originalPath)

    # will parse the HTML page to obtain hrefs of friends.
    hrefs = parseHTML(FULLHTMLPAGE, "friendsurls", 1)
    # will parse hrefs, take only friends' pages and append all_likes to them so we can access their likes.
    friendURLS = parseURLS(hrefs)

    if(numFriendsToScrape == 1):
        driver.get(friendURLS[0])
        time.sleep(3)
        # scroll to get the entire 'likes' page
        for k in range(10):
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        likesPage = driver.page_source
        parseHTML(likesPage, "friendslikes", 1)
    else:
        i = 0
        while(i < numFriendsToScrape and i < len(friendURLS)):
            driver.get(friendURLS[i])
            # scroll to get the entire 'likes' page
            for k in range(10):
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            time.sleep(3)
            likesPage = driver.page_source
            parseHTML(likesPage, "friendslikes", i)
            i += 1


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

    # obtain a friend's likes
    elif(typeOfPage == "friendslikes"):
        # d2edcug0 span contains the name of the liked page
        containers = page_soup.findAll("span", {"class": "d2edcug0"})
        print(f"\n \n \n \n {containers} \n \n \n \n ")
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
            modString += "likes_all"
            newLst.append(modString)

    return newLst


if __name__ == '__main__':

    email = secret.EMAIL
    uname = secret.UNAME
    passw = secret.passw
    numOfFriendsToScrape = 2
    #windowsPath = secret.windowsPath
    linuxPath = secret.linuxPath
    # gets friendsList page
    #getFriendsLikes(uname, email, passw, numOfFriendsToScrape, windowsPath)
    getFriendsLikes(uname, email, passw, numOfFriendsToScrape, linuxPath)

    # print(email)
    # print(passw)
