import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# def unique(l):
#     for e in l:
#         if e in l:

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
i = 0
collections = []
while i < 10:
    driver.execute_script("window.scrollBy(0, 375)")
    time.sleep(1)
    position = 0
    max_position = driver.execute_script("return document.body.scrollHeight")
    elems = driver.find_elements(By.XPATH, "//div[@role='listitem']//div[@class='Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Ranking--collection-name-overflow']")
    for elem in elems:
        collections.append(elem.text)
    while position <= max_position:
        scroll_by_height = 2000
        driver.execute_script("window.scrollBy(0, {})".format(scroll_by_height))
        time.sleep(0.25)
        elems = driver.find_elements(By.XPATH,
                                     "//div[@role='listitem']//div[@class='Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Ranking--collection-name-overflow']")
        for elem in elems:
            collections.append(elem.text)
            # print(elem.text)
        # print(len(elems))
        position += scroll_by_height
    button = driver.find_element(By.XPATH, "//button[@class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 kGCMze hJoTEY']")
    button.click()
    i+=1
collections = set(collections)
print(collections)
print(len(collections))
print(len(collections))

# prepare for csv
c = []
for collection in collections:
    c.append([collection])
collections = c

# open the file in the write mode
f = open('collection_names.csv', 'w+', newline='')

with f:
    write = csv.writer(f)
    write.writerows(collections)

# close the file
f.close()