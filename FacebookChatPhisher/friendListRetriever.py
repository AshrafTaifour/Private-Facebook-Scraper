from seleniumUtil import scrollToBottomOfPage
import re

# Get the Facebook portal that we are using
def getWebsiteFromDriver(driver) -> str:
    m = re.search(r'(https://www\.facebookcorewwwi\.onion)|(https://www\.facebook\.com)', driver.current_url)
    return m.group(0)

# will return the URL of the user's friends list page based on whether they have a user name or not
def getFriendsListPage(uname: str, website: str) -> str:
    # if account has no real username
    retStr = ""
    if 'profile.php?' in uname:
        retStr = f'{website}/{uname}&sk=friends'
    else:
        retStr = f"{website}/{uname}/friends_all"

    return retStr

# Got to friends pages and scroll to load all friends then return back fully loaded page
def getFriendsListHTMLPage(driver, uname: str, maxScrollAttempt=30):
    website = getWebsiteFromDriver(driver)
    yourFriendlistPage = getFriendsListPage(uname, website)
    driver.get(yourFriendlistPage)
    scrollToBottomOfPage(driver, maxScrollAttempt, scrollPauseTime=3)

    # get full HTML page of friends
    return driver.page_source