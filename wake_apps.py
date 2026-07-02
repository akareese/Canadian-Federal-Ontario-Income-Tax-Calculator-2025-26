import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

APP_URLS = [
    "https://ontario-income-tax-calulator-2025-2026-ethanreis.streamlit.app/",
    "https://basketballstatisticalanalysis.streamlit.app/",
    "https://canadian-banking-analysis.streamlit.app/",
]

WAKE_BUTTON_XPATHS = [
    "//button[contains(., 'get this app back up')]",
    "//button[contains(., 'Yes, get this app back up')]",
    "//button[contains(text(), 'Wake up')]",
]

def build_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,800")
    return webdriver.Chrome(options=options)

def visit_app(driver, url):
    try:
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(5)
        for xpath in WAKE_BUTTON_XPATHS:
            try:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(20)
                break
            except NoSuchElementException:
                continue
    except (TimeoutException, WebDriverException):
        pass

def main():
    driver = build_driver()
    try:
        for url in APP_URLS:
            visit_app(driver, url)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
