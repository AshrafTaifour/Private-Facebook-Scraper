from selenium import webdriver
from tbselenium.tbdriver import TorBrowserDriver
from enum import Enum
from functools import partial
from os import getcwd, chdir

#this class adds support functionality for all browsers

class Browser(Enum):
    TOR  = 1
    CHROME = 2
    FIREFOX = 3
    EDGE = 4
    INTERNET_EXPLORER = 5
    OPERA = 6
    SAFARI = 7

SUPPORTED_BROWSER = {
    "Tor": Browser.TOR,
    "Chrome": Browser.CHROME,
    "Firefox": Browser.FIREFOX,
    "Edge": Browser.EDGE,
    "Internet Explorer": Browser.INTERNET_EXPLORER,
    "Opera": Browser.OPERA,
    "Safari": Browser.SAFARI,
}

#gets list of supported browsers
def getSupportedBrowser():
    return list(SUPPORTED_BROWSER.keys())

#raise an exception if browser isn't supported
def invalidDriver(_ = ""):
    raise ValueError("Invalid Browser type selected")

# Tor is the only one that needs explicit access to the browser folder. We assume the driver is in $PATH
def getTorDriver(tor_installation_path: str, driver_path: str):
    # store original path of the directory (tor is changing the path when executing)
    originalPath = getcwd()
    driver = TorBrowserDriver(tor_installation_path, executable_path=driver_path)
    driver.get("https://www.facebookcorewwwi.onion/")
    chdir(originalPath)
    return driver

def getChromeDriver(driver_path: str):
    # will turn off notification for FB to allow webscraping for windows
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    driver.get("http://www.facebook.com")
    return driver

def getFirefoxDriver(driver_path: str):
    driver = webdriver.Firefox(executable_path=driver_path)
    driver.get("http://www.facebook.com")
    return driver

def getEdgeDriver(driver_path: str):
    driver = webdriver.Edge(executable_path=driver_path)
    driver.get("http://www.facebook.com")
    return driver

def getIeDriver(driver_path: str):
    driver = webdriver.Ie(executable_path=driver_path)
    driver.get("http://www.facebook.com")
    return driver

def getOperaDriver(driver_path: str):
    driver = webdriver.Opera(executable_path=driver_path)
    driver.get("http://www.facebook.com")
    return driver

def getSafariDriver(driver_path: str):
    driver = webdriver.Safari(executable_path=driver_path)
    driver.get("http://www.facebook.com")
    return driver

# crude method to guess browser
def guessBrowserFromPath(driver_path: str)-> Browser:
    browser_mode = None
    if  'chromedriver' in driver_path:
        browser_mode = Browser.CHROME
    elif 'geckodriver' in driver_path:
        browser_mode = Browser.FIREFOX
    elif 'MicrosoftWebDriver.exe' in driver_path:
        browser_mode = Browser.EDGE
    elif 'IEDriverServer.exe' in driver_path:
        browser_mode = Browser.INTERNET_EXPLORER
    elif 'operachromiumdriver' in driver_path:
        browser_mode = Browser.OPERA
    elif 'safaridriver' in driver_path: # safari support built in we don't need a path
        browser_mode = Browser.SAFARI
    else:
        invalidDriver()
    return browser_mode

#will obtain and return a driver based on the arguments given
'''
driver_path is the path to the selenium driver 
mode selects what browser you're looking for and match it to the browser class.
tor_installation_path looks for tor brower's path, it will be blank by default in case other browsers are used
 '''
def getDriver(driver_path: str, mode: Browser, tor_installation_path=''):
    driver_selector = {
        Browser.TOR: partial(getTorDriver, tor_installation_path),
        Browser.CHROME: getChromeDriver,
        Browser.FIREFOX: getFirefoxDriver,
        Browser.EDGE: getEdgeDriver,
        Browser.INTERNET_EXPLORER: getIeDriver,
        Browser.OPERA: getOperaDriver,
        Browser.SAFARI: getSafariDriver,
    }
    # Get the function from function selector
    get_browser_driver = driver_selector.get(mode, invalidDriver)
   
    return get_browser_driver(driver_path)
    