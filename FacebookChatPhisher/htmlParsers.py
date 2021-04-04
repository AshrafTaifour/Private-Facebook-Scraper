from bs4 import BeautifulSoup as soup
from lxml import html  # to parse html
#These functions are used to parse data from the retrieved HTML page
# will parse pagesource and return a list of HREFs, parses through friends list page and a friend's likes page
def parseFriendsPage(HTMLPAGE) -> list:
    # use beautifulsoup to parse HTML
    page_soup = soup(HTMLPAGE, "html.parser")
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
    return parseURLS(hrefs)

def parseLikesPage(HTMLPAGE, friendNumber: int, outputPath: str):
     # use beautifulsoup to parse HTML
    page_soup = soup(HTMLPAGE, "html.parser")
    # d2edcug0 span contains the name of the liked page
    containers = page_soup.findAll("span", {"class": "d2edcug0"})

    # save the page to local storage for local parsing
    with open(f"{outputPath}/friendLikesPage{friendNumber}.html", "w", encoding='utf-8') as file:
        file.write(str(containers))


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

