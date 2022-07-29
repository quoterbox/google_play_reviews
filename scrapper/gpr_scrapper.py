import re
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin


class GPRScrapper:
    __review_num = 1
    __main_xpath = ""

    reviews = []

    # 0 - maximum
    count_reviews = 10,

    language = "en"
    xpath_options = {
        "app_name_xpath": "",
        "review_link_xpath": "",
        "modal_window_name_xpath": "",
        "first_review": {
            "review_body": "",
            "name": "",
            "date": "",
            "rating": "",
            "helpful_count": "",
            "text": "",
        },
        "second_review": {
            "review_body": "",
        },
    }
    regexp_xpath_options = {
        "review_body": "",
        "name": "",
        "date": "",
        "rating": "",
        "helpful_count": "",
        "text": "",
    }
    time_options = {
        "delay_before_open_modal": [5, 10],
        "delay_before_close": [5, 10],
        "delay_between_review": [1, 3]
    }
    scroll_options = {
        "scroll_origin_x_offset": [0, 50],
        "scroll_origin_y_offset": [0, 50],
        "scroll_delta_x": [0, 50],
        "scroll_delta_y": [0, 50],
    }

    def __init__(self, driver: webdriver, options: {}):
        self.driver = driver
        self.actions = ActionChains(self.driver)
        self.__set_count_reviews(options["count_reviews"])
        self.__set_language(options["language"])
        self.__set_xpath_options(options["xpath_options"])
        self.__set_time_options(options["time_options"])
        self.__set_scroll_options(options["scroll_options"])

        self.__main_xpath = self.__find_main_xpath(
            options["xpath_options"]["first_review"]["review_body"],
            options["xpath_options"]["second_review"]["review_body"]
        )

        self.__set_regexp_xpath_options(self.__main_xpath, options["xpath_options"]["first_review"])

    def __set_regexp_xpath_options(self, main_xpath: str, first_review: {}):
        for key, value in first_review.items():
            self.regexp_xpath_options[key] = value.replace(main_xpath, "%s")
            self.regexp_xpath_options[key] = re.sub(r'(%s)(\[\d+])(.*)', r'\1[%d]\3', self.regexp_xpath_options[key])

    def __set_count_reviews(self, count_reviews: int):
        self.count_reviews = count_reviews

    def __set_language(self, language: str):
        self.language = language

    def __set_output_file(self, output_file: {}):
        self.fields = output_file

    def __set_xpath_options(self, xpath_options: {}):
        self.xpath_options = xpath_options

    def __set_time_options(self, time_options: {}):
        self.time_options = time_options

    def __set_scroll_options(self, scroll_options: {}):
        self.scroll_options = scroll_options

    def __get_reviews_from_app(self, app_link: str) -> []:

        reviews = []

        app_link = self.__change_language_in_link(app_link)

        # Step 1
        self.driver.get(app_link)

        # Step 2
        app_name = self.driver.find_element(By.XPATH, self.xpath_options["app_name_xpath"]).text

        # Step 3
        review_link = self.driver.find_element(By.XPATH, self.xpath_options["review_link_xpath"])

        self.__sleep(*self.time_options["delay_before_open_modal"])

        # Step 4
        self.__open_modal_window(review_link)

        # Step 5
        review_num = 1
        while True:
            review = self.__get_review_from_app(review_num)
            review['app_name'] = str(app_name)
            review['app_link'] = app_link
            reviews.append(review)

            if self.count_reviews <= review_num:
                break

            review_num = review_num + 1
            self.__sleep(*self.time_options["delay_between_review"])
        return reviews

    def __get_review_from_app(self, review_num: int) -> {}:

        review = {}

        for field_name, value in self.regexp_xpath_options.items():
            field = self.__find_review_field(review_num, field_name)

            if field:
                if field_name == "review_body":
                    self.__scroll_to_review(field)
                elif field_name == "rating":
                    review[field_name] = field.get_attribute("aria-label")
                else:
                    review[field_name] = field.text
            else:
                review[field_name] = "None"

        return review

    def __find_review_field(self, review_num: int, field_name: str) -> WebElement:
        try:
            field = self.driver.find_element(By.XPATH, self.regexp_xpath_options[field_name] % (self.__main_xpath, review_num))

            if field_name == "rating":
                print("%s: %s" % (field_name, field.get_attribute("aria-label")))
            elif field_name != "review_body":
                print("%s: %s" % (field_name, field.text))
            return field
        except NoSuchElementException:
            print("%s for review num - %d - has not been found!" % (field_name, review_num))
            pass

    def __open_modal_window(self, review_link: WebElement):
        scroll_to_reviews = ScrollOrigin(review_link, 0, 0)
        self.actions.scroll_to_element(review_link).perform()
        self.actions.scroll_from_origin(scroll_to_reviews, 0, 500)
        self.actions.move_to_element(review_link)
        self.actions.click(review_link)
        self.actions.perform()

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, self.xpath_options["modal_window_name_xpath"])))

    def __scroll_to_review(self, review_element: WebElement):
        scroll_to_review = ScrollOrigin(
            review_element,
            random.randint(*self.scroll_options["scroll_origin_x_offset"]),
            random.randint(*self.scroll_options["scroll_origin_y_offset"])
        )
        self.actions.scroll_from_origin(
            scroll_to_review,
            random.randint(*self.scroll_options["scroll_delta_x"]),
            random.randint(*self.scroll_options["scroll_delta_y"])
        ).move_to_element(review_element).perform()

    def __change_language_in_link(self, link: str) -> str:
        return re.sub(r'(.*hl=)(\D{2})(.*)?', (r'\1%s\3') % self.language, link)

    def get_reviews(self) -> []:
        return self.reviews

    def run(self, app_links: []):
        for app_link in app_links:
            self.reviews += self.__get_reviews_from_app(app_link)

        self.__sleep(*self.time_options["delay_before_close"])
        self.driver.close()

    @staticmethod
    def __find_main_xpath(first_xpath: str, second_xpath: str) -> str:
        if len(first_xpath) != len(second_xpath):
            raise ValueError('XPATH for first and second reviews has different length! They must be the same length.')

        position = 0
        for key, letter in enumerate(first_xpath):
            if letter != second_xpath[key]:
                position = key
                break

        if not position:
            raise ValueError('Have no a difference between first and second reviews xpath! '
                             'They must have a different digits for some tag like "/html/div[1]" and "/html/div[2]".')

        return first_xpath[:position - 1]

    @staticmethod
    def __sleep(min_time: int, max_time: int):
        time.sleep(random.randint(min_time, max_time))

    @staticmethod
    def clear_string(string: str) -> str:
        special_characters = [";", "\t", "\n", "\r", "\n\r", "<", ">"]
        return ''.join(filter(lambda i: i not in special_characters, string)).strip()
