from selenium.webdriver.common.keys import Keys
import time

#Helper function for Selenium 
# Scroll to end of page 
def scrollToBottomOfPage(driver, maxScrollAttempt: int, scrollPauseTime = 2):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    elm = driver.find_element_by_tag_name('html')
    for i in range(maxScrollAttempt):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
 
        # Wait to load page
        time.sleep(scrollPauseTime)
        # Scrolling Up & Down to load more Data
        elm.send_keys(Keys.HOME)
        time.sleep(1)
        elm.send_keys(Keys.END)
        time.sleep(1)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height