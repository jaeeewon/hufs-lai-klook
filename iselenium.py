from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


class SafeSeleniumDriver:
    """
    with SafeSeleniumDriver(command_executor_url) as driver:
        driver.get("https://example.com")
    """

    def __init__(self, command_executor):
        self.command_executor = command_executor
        self.driver = None

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(
            f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Whale/4.34.340.17 Safari/537.36"
        )
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-logging", "enable-automation"]
        )
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.options = chrome_options

    def __enter__(self):
        self.driver = webdriver.Remote(
            command_executor=self.command_executor, options=self.options
        )
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        if self.driver:
            print("closing selenium")
            self.driver.quit()
            self.driver = None
        else:
            print("selenium not running")

        if exc_type:
            print(f"exception: {exc_type}")

        return False
