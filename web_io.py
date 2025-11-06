from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import logging
import os

# from selenium.webdriver.chrome.service import Service
# import tempfile
logging.basicConfig(level=os.getenv("LOG_LEVEL"), force=True)
logger = logging.getLogger(__name__)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--single-process")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

# # 每次创建一个独立的临时用户目录
# user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
# options.add_argument(f"--user-data-dir={user_data_dir}")
# options.binary_location = "/usr/bin/chrome-headless-shell/chrome-headless-shell"

# driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver/chromedriver"),options=options)
driver = webdriver.Chrome(options=options)
driver.get("https://www.nytimes.com/games/wordle/index.html")
logger.debug(f"title: {driver.title}")
# click on the start button
driver.find_element(
    By.XPATH, "/html/body/div[2]/div[1]/div/div/div/div[2]/button[3]"
).click()
sleep(3)

# click on the close button
driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb").click()
sleep(1)

state = driver.find_element(
    By.XPATH, '//*[@id="wordle-app-game"]/div[1]/div/div[1]/div[1]/div'
).get_attribute("data-state")

logger.debug("web_driver loaded")


def click_letter(letter):
    key = driver.find_element(By.XPATH, f'//*[@data-key="{letter}"]')
    # print(key.get_attribute("aria-label"))
    key.click()


def input(word, row):
    for i in range(0, 5, 1):
        click_letter(word[i])
    enter = driver.find_element(By.XPATH, f'//*[@aria-label="enter"]')
    enter.click()
    sleep(3)
    result = []
    blocks = driver.find_elements(By.XPATH, f'//*[@aria-label="Row {row}"]/div/div')
    for i in range(0, 5, 1):
        # result.append(blocks[i].get_attribute("data-state"))
        word_state = blocks[i].get_attribute("data-state")

        if word_state == "absent" and (word[i] in word[:i]) and result[word.index(word[i])] == "present":
           word_state = "present"
        result.append(word_state)
    logger.info(f"try '{word}': {result}")
    return result


if __name__ == "__main__":
    input("touch", 1)
