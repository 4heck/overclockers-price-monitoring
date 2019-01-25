import logging
import re
import time

from conf import settings
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProxyParser:
    """Proxy Parser"""

    logger = logging.getLogger(__name__)

    def get_element_by_css_selector(self, driver, selector):
        """Get element by CSS selector"""
        try:
            element = driver.find_element_by_css_selector(selector)
        except (NoSuchElementException, TimeoutException):
            element = None
        return element

    def get_elements_by_css_selector(self, driver, selector):
        """Get elements by CSS selector"""
        try:
            elements = driver.find_elements_by_css_selector(selector)
        except (NoSuchElementException, TimeoutException):
            elements = []
        return elements

    def parse_proxy(self, country_link, proxy_server=None):
        """Parse proxy"""
        capabilities = {
            "browserName": "chrome",
            "version": "70.0",
            "screenResolution": "1024x600x16",
            "enableVNC": True,
            "enableVideo": False,
            "chromeOptions": {
                'args': [
                    '--disable-notifications',
                    '--disable-logging',
                    '--disable-infobars',
                    '--disable-extensions',
                    '--disable-web-security',
                    '--no-sandbox',
                    # '--headless',
                    '--silent',
                    '--disable-popup-blocking',
                    '--incognito',
                    '--lang=ru',
                    '--ignore-certificate-errors'
                ]
            }
        }

        if proxy_server:
            capabilities['chromeOptions']['args'].append(f'--proxy-server={proxy_server}')

        driver = webdriver.Remote(
            command_executor=settings.SELENOID_HUB,
            desired_capabilities=capabilities)

        # user agent
        ua = UserAgent()
        user_agent = ua.random
        if user_agent:
            capabilities['chromeOptions']['args'].append(f'--user-agent={user_agent}')

        proxies = []

        try:
            # open proxy
            driver.get(country_link)

            # wait until page would be loaded
            option_selector = '#xpp option:last-child'
            option_wait = WebDriverWait(driver, 30)
            option_element = option_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, option_selector))
            )

            if option_element:
                option_element.click()

            time.sleep(7)

            # wait until page would be loaded
            tr_selector = 'td > table > tbody > tr[class^="spy1x"]'
            tr_wait = WebDriverWait(driver, 30)
            tr_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, tr_selector))
            )

            tr_elements = self.get_elements_by_css_selector(driver, tr_selector)

            pattern = re.compile(r'(?P<value>[0-9]+(?:\.[0-9]+){3}:[0-9]+)\s+(?P<type>HTTPS|HTTP|SOCKS5)')

            for tr_element in tr_elements:
                result = pattern.search(tr_element.text)
                if result:
                    proxy_value = result.group('value')
                    proxy_type = result.group('type')
                    if proxy_value and proxy_type:
                        proxies.append({
                            'value': proxy_value,
                            'type': proxy_type
                        })
        except (WebDriverException, TimeoutException) as err:
            self.logger.error(str(err))
        finally:
            try:
                driver.quit()
            except (WebDriverException, TimeoutException) as err:
                self.logger.error(str(err))
        return proxies
