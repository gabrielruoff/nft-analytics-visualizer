import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")
from selenium.webdriver.common.keys import Keys


def scrape_collection_names(num_pages=1):
    driver = webdriver.Firefox()
    driver.get("https://opensea.io/rankings")
    i = 0
    collections = []
    for i in range(num_pages):
        driver.execute_script("window.scrollBy(0, 375)")
        time.sleep(1)
        position = 0
        max_position = driver.execute_script("return document.body.scrollHeight")
        elems = driver.find_elements(By.XPATH,
                                     "//a[@class='styles__StyledLink-sc-l6elh8-0 ekTmzq Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 Itemreact__ItemBase-sc-1idymv7-0 styles__FullRowContainer-sc-12irlp3-0 bnxsDk jYqxGr dCVDRE lcvzZN fresnel-greaterThanOrEqual-xl']")
        for elem in elems:
            href = elem.get_attribute("href").split('/')[-1]
            collections.append(href)
        while position <= max_position:
            scroll_by_height = 2000
            driver.execute_script("window.scrollBy(0, {})".format(scroll_by_height))
            time.sleep(0.25)
            elems = driver.find_elements(By.XPATH,
                                         "//a[@class='styles__StyledLink-sc-l6elh8-0 ekTmzq Blockreact__Block-sc-1xf18x6-0 Flexreact__Flex-sc-1twd32i-0 Itemreact__ItemBase-sc-1idymv7-0 styles__FullRowContainer-sc-12irlp3-0 bnxsDk jYqxGr dCVDRE lcvzZN fresnel-greaterThanOrEqual-xl']")
            for elem in elems:
                href = elem.get_attribute("href").split('/')[-1]
                collections.append(href)
            position += scroll_by_height
        button = driver.find_element(By.XPATH,
                                     "//button[@class='Blockreact__Block-sc-1xf18x6-0 Buttonreact__StyledButton-sc-glfma3-0 kGCMze hJoTEY']")
        button.click()
    driver.quit()
    collections = set(collections)
    return collections


def export_collection_names_to_csv(collections, filename):
    # prepare for csv
    c = []
    for collection in collections:
        c.append([collection])

    # open the file in the write mode
    f = open(filename, 'w+', newline='')

    with f:
        write = csv.writer(f)
        write.writerows(c)

    # close the file
    f.close()


collections = scrape_collection_names(20)
print(collections)
print(len(collections))
print(len(collections))
export_collection_names_to_csv(collections, 'collection_names.csv')