import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()

# google_play_review_scrapper = GPRScrapper(
#     driver,
#     {
#         "language": "ru", #en
#         "review_link_xpath": "//h2[contains(text(), 'Оценки и отзывы')]/../../../../div//i[contains(text(), 'arrow_forward')]",
#         "xpath_setup":{
#             "first_review_xpath": {
#                 "self": "",
#                 "name": "",
#                 "date": "",
#                 "rating": "",
#                 "helpful_count": "",
#                 "text": "",
#             },
#             "second_review": {
#                 "xpath": "",
#                 "name": "",
#                 "date": "",
#                 "rating": "",
#                 "helpful_count": "",
#                 "text": "",
#             },
#         },
#         "output_file": {
#             "name": "reviews.csv",
#             "fields": {
#                 "name": "Name",
#                 "date": "Date",
#                 "rating": "Rating",
#                 "helpful_count": "Helpful reviews count",
#                 "text": "Text",
#             }
#         }
#     }
# )
#
# app_links = [
#     "https://play.google.com/store/apps/details?id=com.coinbase.android&hl=ru",
#     "https://play.google.com/store/apps/details?hl=en&id=com.coinbase.android",
#     "https://play.google.com/store/apps/details?hl=en&id=org.toshi",
#     "https://play.google.com/store/apps/details?hl=en&id=com.binance.dev",
#     "https://play.google.com/store/apps/details?hl=en&id=co.mona.android",
#     "https://play.google.com/store/apps/details?hl=en&id=com.bybit.app",
#     "https://play.google.com/store/apps/details?hl=en&id=io.metamask",
#     "https://play.google.com/store/apps/details?hl=en&id=com.wallet.crypto.trustapp",
#     "https://play.google.com/store/apps/details?hl=en&id=com.nexowallet",
#     "https://play.google.com/store/apps/details?hl=en&id=br.com.mercadobitcoin.android",
#     "https://play.google.com/store/apps/details?hl=en&id=com.nicehash.metallum",
#     "https://play.google.com/store/apps/details?hl=en&id=com.whitebit.android",
#     "https://play.google.com/store/apps/details?hl=en&id=com.coinsbit.coinsbit",
#     "https://play.google.com/store/apps/details?hl=en&id=com.wrx.wazirx",
#     "https://play.google.com/store/apps/details?hl=en&id=com.coindcx.btc",
#     "https://play.google.com/store/apps/details?hl=en&id=id.co.bitcoin",
#     "https://play.google.com/store/apps/details?hl=en&id=co.bitx.android.wallet",
#     "https://play.google.com/store/apps/details?hl=en&id=pro.huobi",
#     "https://play.google.com/store/apps/details?hl=en&id=com.digifinex.app",
#     "https://play.google.com/store/apps/details?hl=en&id=com.gateio.gateio",
#     "https://play.google.com/store/apps/details?hl=en&id=com.stormgain.mobile",
#     "https://play.google.com/store/apps/details?hl=en&id=com.mexcpro.client",
#     "https://play.google.com/store/apps/details?hl=en&id=com.app.xt",
#     "https://play.google.com/store/apps/details?hl=en&id=com.kubi.kucoin",
#     "https://play.google.com/store/apps/details?hl=en&id=com.blockfolio.blockfolio"
# ]
#
# google_play_review_scrapper.run(app_links)
# driver.close()



driver.get("https://play.google.com/store/apps/details?hl=ru&id=com.coinbase.android&gl=US")#&gl=RU

review_link_xpath = "//h2[contains(text(), 'Оценки и отзывы')]/../../../../div//i[contains(text(), 'arrow_forward')]"
review_link = driver.find_element(By.XPATH, review_link_xpath)

time.sleep(random.randint(1, 3))

scroll_to_reviews = ScrollOrigin(review_link, 0, 0)

actions = ActionChains(driver)
actions.scroll_to_element(review_link).perform()
actions.scroll_from_origin(scroll_to_reviews, 0, 500)
actions.move_to_element(review_link)
actions.click(review_link)
actions.perform()

modal_window = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]")))

review_number = 1
main_xpath = "html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div"
reviews = []

# fieldnames = ['Name', 'Date', 'Rating', 'Helpful count', 'Text']
fieldnames = ['name', 'date', 'rating', 'helpful_count', 'text']


with open("out.csv", "w", encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=fieldnames)
    writer.writerow({
        'name': 'Name',
        'date': 'Date',
        'rating': 'Rating',
        'helpful_count': 'Helpful count',
        'text': 'Text',
    })

while True:
        review_element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "%s[%d]" % (main_xpath, review_number))))

        if review_element:

            name = ""
            date = ""
            rating = ""
            helpful_count = ""
            text = ""

            print("Review num-%d has been found" % review_number)

            scroll_to_review = ScrollOrigin(review_element, 0, random.randint(100, 200))
            actions.scroll_from_origin(scroll_to_review, 0, 500).move_to_element(review_element).perform()

            # name = driver.find_element(By.XPATH, "%s[%d]/header/div[1]/div[1]" % (main_xpath, review_number)).text
            try:
                name = driver.find_element(By.XPATH, "%s[%d]/header/div[1]/div[1]" % (main_xpath, review_number)).text
                print("Name: %s" % name)
            except NoSuchElementException:
                print("ELEMENT -name- has not been found!")
                pass

            # name = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "%s[%d]/header/div[1]/div[1]" % (main_xpath, review_number)))).text
            # print("Name: %s" % name)


            try:
                date = driver.find_element(By.XPATH, "%s[%d]/header/div[2]/span" % (main_xpath, review_number)).text
                print("Date: %s" % date)
            except NoSuchElementException:
                print("ELEMENT -date- has not been found!")
                pass

            # date = driver.find_element(By.XPATH, "%s[%d]/header/div[2]/span" % (main_xpath, review_number)).text
            # date = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "%s[%d]/header/div[2]/span" % (main_xpath, review_number)))).text
            # print("Date: %s" % date)


            try:
                rating = driver.find_element(By.XPATH, "%s[%d]/header/div[2]/div" % (main_xpath, review_number)).get_attribute("aria-label")
                print("Rating: %s" % rating)
            except NoSuchElementException:
                print("ELEMENT -rating- has not been found!")
                pass

            # rating = driver.find_element(By.XPATH, "%s[%d]/header/div[2]/div" % (main_xpath, review_number)).get_attribute("aria-label")
            # rating = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "%s[%d]/header/div[2]/div" % (main_xpath, review_number)))).get_attribute("aria-label")
            # print("Rating: %s" % rating)


            try:
                helpful_count = driver.find_element(By.XPATH, "%s[%d]/div[2]/div" % (main_xpath, review_number)).text
                print("Helpful count: %s" % helpful_count)
            except NoSuchElementException:
                print("ELEMENT -helpful_count- has not been found!")
                pass

            # helpful_count = driver.find_element(By.XPATH, "%s[%d]/div[2]/div" % (main_xpath, review_number)).text
            # helpful_count = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "%s[%d]/div[2]/div" % (main_xpath, review_number)))).text
            # print("Helpful count: %s" % helpful_count)


            try:
                text = driver.find_element(By.XPATH, "%s[%d]/div[1]" % (main_xpath, review_number)).text
                print("Text: %s" % text)
            except NoSuchElementException:
                print("ELEMENT -text- has not been found!")
                pass

            # text = driver.find_element(By.XPATH, "%s[%d]/div[1]" % (main_xpath, review_number)).text
            # text = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located(
            #         (By.XPATH, "%s[%d]/div[2]/div" % (main_xpath, review_number)))).text
            # print("Text: %s" % text)

            with open("out.csv", "a", encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, delimiter=';', fieldnames=fieldnames)
                writer.writerow({
                    'name': name,
                    'date': date,
                    'rating': rating,
                    'helpful_count': helpful_count,
                    'text': text,
                })

            time.sleep(random.randint(1, 3))

            review_number = review_number + 1

        else:

            print("Review num-%d has not been found!" % review_number)
            break



time.sleep(random.randint(4, 7))

driver.close()
