# Get reviews from Google Play for any Apps with Selenium

The video below shows how review extractor works:

https://user-images.githubusercontent.com/8583337/182228190-779d7df9-654a-4558-87a4-542a8bfc522b.mp4


## Description of the crawler

1. This is a simple Python class to get reviews from Google Play for any Apps without any API.
2. GPRScrapper uses Selenium library for Python and chromedriver as well (or any other for your web browser).
3. GPRScrapper allows you to receive data in the desired language.
4. It's easy to use in any browser with XPATH copy and paste.

## Setup

### How to start python script in shell

1. Install python 3.7+ https://www.python.org/downloads/windows/ (or version for you OS)
2. Install pipenv `pip install --user pipenv`. Docs are here: https://github.com/pypa/pipenv
3. To install all packages run this command: `pipenv install`
4. To start python script: `pipenv run py main.py` (for windows)
5. Download Chromedriver for yor own Google Chrome version (or your own, Gecko driver for Firefox etc.), from this page:
https://chromedriver.chromium.org and put it next to the `main.py` file.

## How it works:

1. Copy and past you app link from Google Play like an arg with list type in `gprscrapper.run(["YOUR_OWN_APP_LINK", "YOUR_OWN_APP_LINK"])` method.
2. Copy and past XPATH from browser (**Right-click on a page element -> Copy -> Copy full Xpath**).
3. When script is finished, you can extract reviews from instance of GPRScrapper object with method `gprscrapper.get_reviews()` 
4. For example, you can save reviews into CSV file. 

### Example to set up GPRScrapper object:

You can use either the browser window or not with this option for Selenium driver:
`chrome_options.headless = True`

    google_play_review_scrapper = GPRScrapper(
        # selenium driver
        driver,
        {
            # 0 - maximum
            "count_reviews": 500,
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
        })

###  Put your own links to the run method:
    google_play_review_scrapper.run([
        "https://play.google.com/store/apps/details?hl=en&id=org.app",
        "https://play.google.com/store/apps/details?hl=en&id=com.some.app",
    ])

### After executing of `google_play_review_scrapper.run()` 
You can extract reviews from the object with `gprscrapper.get_reviews()` and save them to a file.
