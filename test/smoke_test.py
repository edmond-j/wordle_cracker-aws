import tempfile
from selenium import webdriver
print("imported webdriver")
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")

# 每次创建一个独立的临时用户目录
# user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
# chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
# print("user_data_dir:", user_data_dir)

driver = webdriver.Chrome(options=chrome_options)
print("driver initialized ")
def lambda_handler(event, context):
    driver.get("https://www.google.com")
    print("event is:", event.key1)
    print(driver.title)
    driver.quit()
