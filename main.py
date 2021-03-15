from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as soup
import time
from lxml import html #to parse html
from secretDirectory import secret

#username is name in url
def getFriendsLikes(uname, email, passw, numFriendsToScrape):
    # will turn off notification for FB to allow webscraping
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome('C:/Users/Ashraf/chromedriver.exe', options=chrome_options)

    # will open the webpage
    driver.get("http://www.facebook.com")

    # target username field
    usernameBox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    passwordBox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    # enters username and password
    usernameBox.clear()
    usernameBox.send_keys(email)
    passwordBox.clear()
    passwordBox.send_keys(passw)

    # login button is targeted and clicked
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    #
    time.sleep(5)
    driver.get(f"https://www.facebook.com/{uname}/friends_all")

    # scroll 10 times to get all friends on page
    for j in range(0, 10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    #get full HTML page of friends
    FULLHTMLPAGE = driver.page_source

    #will parse the HTML page to obtain hrefs of friends.
    hrefs = parseHTML(FULLHTMLPAGE, "friendsurls", 1)
    #will parse hrefs, take only friends' pages and append all_likes to them so we can access their likes.
    friendURLS = parseURLS(hrefs)

    if(numFriendsToScrape == 1):
        driver.get(friendURLS[0])
        time.sleep(3)
        #scroll to get the entire 'likes' page
        for k in range(10):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        likesPage = driver.page_source
        parseHTML(likesPage, "friendslikes", 1)
    else:
        i = 0
        while(i < numFriendsToScrape and i < len(friendURLS)):
            driver.get(friendURLS[i])
            # scroll to get the entire 'likes' page
            for k in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            time.sleep(3)
            likesPage = driver.page_source
            parseHTML(likesPage, "friendslikes", i)
            i += 1



    #go through all friends' likes pages and obtain a list of things they like
    #seems like class: kvgmc6g5 is used for the description of the like and the like itself has span class: d2edcug0 for key, div class kvgmc6g5 for
    #NOTE: this must be in the same scope since we need to be logged in to do this activity.
    #for friendPage in friendURLs:
    #     driver.get(friendPage) #go to friend's likes page
    #     #scroll to get all entries
    #     for j in range(0, 10):
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(3)
    #     likesPage = driver.page_source



#will parse pagesource and return a list of HREFs, parses through friends list page and a friend's likes page
def parseHTML(HTMLPAGE, typeOfPage: str, friendNumber: int):
    #use beautifulsoup to parse HTML
    page_soup = soup(HTMLPAGE, "html.parser")

    #obtain your friends' URLs
    if(typeOfPage == "friendsurls"):
        #oajrlxb2 class contains many URLS that will be useful for finding friends' page URLs
        containers = page_soup.findAll("a", {"class": "oajrlxb2"})
        #save the page to local storage for local parsing
        with open("friendListPage.html", "w", encoding='utf-8') as file:
            file.write(str(containers))
        tree = html.parse("friendListPage.html")
        html.tostring(tree)
        hrefs = tree.xpath('//@href')

    #obtain a friend's likes
    elif(typeOfPage == "friendslikes"):
        # d2edcug0 span contains the name of the liked page
        containers = page_soup.findAll("span", {"class": "d2edcug0"})
        # save the page to local storage for local parsing
        with open(f"friendLikesPage{friendNumber}.html", "w", encoding='utf-8') as file:
            file.write(str(containers))
        tree = html.parse(f"friendLikesPage{friendNumber}.html")
        html.tostring(tree)
        hrefs = tree.xpath('//@href')
    else:
        print("INVALID INPUT")


    return hrefs




#parses through the list of URLS
def parseURLS(lst: list) -> list:
    newLst = []
    for link in lst:
        if"friends_mutual" in link:
            size = len(link)
            modString = link[:size - 14]
            modString += "likes_all"
            newLst.append(modString)
    #for i in range (0, len(lst), 2):
    #    newLst.append(lst[i])

    return newLst

#def parseLikesPage(page ):






if __name__ == '__main__':

    email = secret.EMAIL
    uname = secret.UNAME
    passw = secret.passw
    numOfFriendsToScrape = 1

    # gets friendsList page
    getFriendsLikes(uname, email, passw, numOfFriendsToScrape)

    # from tbselenium.tbdriver import TorBrowserDriver
    #
    # with TorBrowserDriver("/path/to/TorBrowserBundle/") as driver:
    #     driver.get('https://check.torproject.org')
    #https://manivannan-ai.medium.com/selenium-with-tor-browser-using-python-7b3606b8c55c









