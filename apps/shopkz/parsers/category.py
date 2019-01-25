import logging
from io import StringIO

import requests
from conf import settings
from furl import furl
from lxml import html


class CategoryParser:
    """Category Parser"""

    logger = logging.getLogger(__name__)

    def get_selector_root(self, link, proxy_server=None):
        """Get selector root"""
        try:
            proxies = {}

            if proxy_server:
                proxies = {
                    'http': f'http://{proxy_server}',
                    'https': f'https://{proxy_server}',
                }

            response = requests.get(link, timeout=20, proxies=proxies)
            response.encoding = 'utf-8'
            stream = StringIO(response.text)
            root = html.parse(stream).getroot()
            return root
        except Exception:
            return None

    def get_element_by_selector(self, element, selector):
        """Get element by selector"""
        try:
            elements = element.cssselect(selector)
            if len(elements) > 0:
                return elements[0]
        except Exception as err:
            self.logger.warning(str(err))
        return None

    def get_elements_by_selector(self, element, selector):
        """Get elements by selector"""
        try:
            elements = element.cssselect(selector)
            return elements
        except Exception as err:
            self.logger.warning(str(err))
        return None

    def parse(self, root):
        """Parse root"""
        last_page_number = 1
        products = []

        shopkz_main_url = settings.SHOPKZ_MAIN_URL.rstrip('/')

        try:
            # last_page_number
            page_number_selector = '.bx-pagination  li:nth-last-child(2) a'
            page_number_element = self.get_element_by_selector(root, page_number_selector)
            if page_number_element:
                page_number_link = page_number_element.get('href', '')
                page_number_link = furl(page_number_link)
                try:
                    last_page_number = int(page_number_link.args.get('PAGEN_1', 1))
                except ValueError as err:
                    self.logger.error(err)

            # products
            product_selector = '.bx_catalog_list_home .bx_catalog_item .bx_catalog_item_title a'
            product_elements = self.get_elements_by_selector(root, product_selector)

            for product_element in product_elements:
                # init product
                href = product_element.get('href')
                product = {
                    'name': product_element.text_content(),
                    'link': f'{shopkz_main_url}{href}'
                }

                # append product to list
                products.append(product)

        except Exception as err:
            self.logger.warning(str(err))
        return {
            'last_page_number': last_page_number,
            'products': products
        }
