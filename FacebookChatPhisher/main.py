from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as soup
import time
from lxml import html  # to parse html
import re

def getWebsiteFromDriver(driver) ->str:
    m = re.search(r'(https://www\.facebookcorewwwi\.onion)|(https://www\.facebook\.com)', driver.current_url)
    return m.group(0)

def getFriendsListHTMLPage(driver, uname: str):
    website = getWebsiteFromDriver(driver)
    yourFriendlistPage = getFriendsListPage(uname, website)
    driver.get(yourFriendlistPage)

    # scroll 10 times to get all friends on page
    for j in range(0, 10):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # get full HTML page of friends
    return driver.page_source



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
    # change directory back to the original so we can save friendsURLs page and likePages in the same directory as the project.


# will return the URL of the user's friends list page based on whether they have a user name or not
def getFriendsListPage(uname: str, website: str):
    # if account has no real username
    retStr = ""
    if 'profile.php?' in uname:
        retStr = f'{website}/{uname}&sk=friends'
    else:
        retStr = f"{website}/{uname}/friends_all"

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
    # also get driver file to use 
    from driver import getDriver, Browser

    email=secret.EMAIL
    passw=secret.passw
    uname = secret.UNAME
    tor_path=secret.torBrowserPath
    driver_path=secret.exePath
    numOfFriendsToScrape = 2
    driver = getDriver(driver_path, Browser.TOR, tor_path)

    loginToFacebook(driver, email, passw)
    time.sleep(8)

    FULLHTMLPAGE = getFriendsListHTMLPage(driver, uname)

    # will parse the HTML page to obtain hrefs of friends.
    friendURLS = parseHTML(FULLHTMLPAGE, "friendsurls", 1)

    scrapeLikePages(driver, friendURLS, numOfFriendsToScrape)
