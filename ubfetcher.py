import logging
from sys import stdout

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

RESERVE_URL = 'https://www.ub.tum.de/arbeitsplatz-reservieren'

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Driver:
    driver = None

    def start_webdriver(self):
        options = Options()
        # TODO: uncomment for production
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1200")
        logger.info("starting chrome driver")
        self.driver = webdriver.Chrome(options=options)
        logger.info("chrome driver started")
        self.driver.implicitly_wait(3)

    def visit_reservation_overview(self):
        self.driver.get(RESERVE_URL)

    def extract_bib_status(self) -> []:
        table_rows = self.driver.find_elements(By.XPATH, "//*[@id='block-system-main']/div/div/div[2]/table/tbody/tr")
        for table_row in table_rows:
            cells = table_row.find_elements(By.TAG_NAME, "td")

            if len(cells) != 4:
                logger.error("could not parse row: " + table_row.text)
                continue

            name = cells[0].text
            date = cells[1].text
            timespan = cells[2].text
            status = cells[3].text
            reservation_link = None

            if status != "ausgebucht":
                reservation_link = cells[3].find_element(By.TAG_NAME, "a").get_attribute("href")

            print(
                f'{name}: {date} - {timespan} -> {status} / {reservation_link}')

    def quit(self):
        logger.info("quitting chrome driver...")
        self.driver.quit()


if __name__ == "__main__":
    driver = Driver()
    driver.start_webdriver()
    driver.visit_reservation_overview()
    driver.extract_bib_status()
    driver.quit()
