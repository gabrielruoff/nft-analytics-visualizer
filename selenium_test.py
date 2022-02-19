import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# def scroll_down(driver):
#     """A method for scrolling the page."""
#
#     # Get scroll height.
#     last_height = driver.execute_script("return document.body.scrollHeight")
#
#     while True:
#
#         # Scroll down to the bottom.
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#         # Wait to load the page.
#         time.sleep(2)
#
#         # Calculate new scroll height and compare with last scroll height.
#         new_height = driver.execute_script("return document.body.scrollHeight")
#
#         if new_height == last_height:
#
#             break
#
#         last_height = new_height

driver = webdriver.Firefox()
driver.get("https://opensea.io/rankings")
driver.execute_script("window.scrollBy(0, 375)")
time.sleep(1)
elems = driver.find_elements(By.XPATH, "//div[@role='listitem']//div[@class='Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Ranking--collection-name-overflow']")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
position = 0
max_position = driver.execute_script("return document.body.scrollHeight")
collections = []
while(position <= max_position):
    driver.execute_script("window.scrollBy(0, 1400)")
    time.sleep(1)
    elems = driver.find_elements(By.XPATH,
                                 "//div[@role='listitem']//div[@class='Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Ranking--collection-name-overflow']")
    for elem in elems:
        collections.append(elems)
        print(elem.text)
    print(len(elems))

print(len(collections))
print(len(sorted(set(collections))))