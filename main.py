import csv
from selenium import webdriver
from scrapper.gpr_scrapper import GPRScrapper

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.71")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-setuid-sandbox')

# Yes / No browser visualization
chrome_options.headless = True

driver = webdriver.Chrome(options=chrome_options)

google_play_review_scrapper = GPRScrapper(
    driver,
    {
        # 0 - maximum
        "count_reviews": 10,
        # en/ru
        "language": "en",
        # you should copy these xpaths from your browser (right click and select "Inspect element")
        "xpath_options": {
            "app_name_xpath": "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1",
            "review_link_xpath": "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/header/div/div[2]/button/i",
            "modal_window_name_xpath": "/html/body/div[4]/div[2]/div/div/div/div/div[1]/div/div/h5",
            "first_review": {
                "review_body": "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]",
                "name": "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/header/div[1]/div[1]/div",
                "date": "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/header/div[2]/span",
                "rating": "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/header/div[2]/div",
                "helpful_count": "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]/div",
                "text": "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[1]",
            },
            "second_review": {
                "review_body": "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div[2]",
            },
        },
        # time delays will be randomly selected between min and max value
        "time_options": {
            "delay_before_open_modal": [5, 10],
            "delay_before_close": [5, 10],
            "delay_between_review": [1, 3]
        },
        # pixels offsets will be randomly selected between min and max value
        "scroll_options": {
            "scroll_origin_x_offset": [0, 50],
            "scroll_origin_y_offset": [0, 50],
            "scroll_delta_x": [0, 50],
            "scroll_delta_y": [0, 50],
        }
    }
)

# links for example
google_play_review_scrapper.run([
    "https://play.google.com/store/apps/details?hl=en&id=com.coinbase.android",
    "https://play.google.com/store/apps/details?hl=en&id=org.toshi",
    "https://play.google.com/store/apps/details?hl=en&id=com.binance.dev",
    "https://play.google.com/store/apps/details?hl=en&id=co.mona.android",
    "https://play.google.com/store/apps/details?hl=en&id=com.bybit.app",
    "https://play.google.com/store/apps/details?hl=en&id=io.metamask",
    "https://play.google.com/store/apps/details?hl=en&id=com.wallet.crypto.trustapp",
    "https://play.google.com/store/apps/details?hl=en&id=com.nexowallet",
    "https://play.google.com/store/apps/details?hl=en&id=br.com.mercadobitcoin.android",
    "https://play.google.com/store/apps/details?hl=en&id=com.nicehash.metallum",
    "https://play.google.com/store/apps/details?hl=en&id=com.whitebit.android",
    "https://play.google.com/store/apps/details?hl=en&id=com.coinsbit.coinsbit",
    "https://play.google.com/store/apps/details?hl=en&id=com.wrx.wazirx",
    "https://play.google.com/store/apps/details?hl=en&id=com.coindcx.btc",
    "https://play.google.com/store/apps/details?hl=en&id=id.co.bitcoin",
    "https://play.google.com/store/apps/details?hl=en&id=co.bitx.android.wallet",
    "https://play.google.com/store/apps/details?hl=en&id=pro.huobi",
    "https://play.google.com/store/apps/details?hl=en&id=com.digifinex.app",
    "https://play.google.com/store/apps/details?hl=en&id=com.gateio.gateio",
    "https://play.google.com/store/apps/details?hl=en&id=com.stormgain.mobile",
    "https://play.google.com/store/apps/details?hl=en&id=com.mexcpro.client",
    "https://play.google.com/store/apps/details?hl=en&id=com.app.xt",
    "https://play.google.com/store/apps/details?hl=en&id=com.kubi.kucoin",
    "https://play.google.com/store/apps/details?hl=en&id=com.blockfolio.blockfolio"
])

output_file = {
    "name": "reviews.csv",
    "fields": {
        "app_name": "App name",
        "app_link": "App link",
        "name": "Name",
        "date": "Date",
        "rating": "Rating",
        "helpful_count": "Helpful reviews count",
        "text": "Text",
    }
}

with open(output_file["name"], "w", encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=output_file["fields"].keys())
    writer.writerow(output_file["fields"])

with open(output_file["name"], "a", encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, delimiter=';', fieldnames=output_file["fields"].keys())
    for review in google_play_review_scrapper.get_reviews():
        writer.writerow(review)

print("Reviews has been successfully saved to the file!")
