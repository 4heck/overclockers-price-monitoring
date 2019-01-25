import logging
from io import StringIO

import requests
from lxml import html


class ProductParser:
    """Product Parser"""

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
        product_dict = {}

        try:
            # prices
            prices = []
            price_elements = self.get_elements_by_selector(root, '.bx-more-prices > ul > li')

            for price_element in price_elements:
                title = self.get_element_by_selector(price_element, '.bx-more-price-title')
                text = self.get_element_by_selector(price_element, '.bx-more-price-text')
                if title is not None and text is not None:
                    prices.append({'title': title.text_content(), 'text': text.text_content()})

            # price
            price = list(filter(lambda item: 'Цена по прайсу' in item.get('title'), prices))

            if len(price):
                product_dict['price'] = price[0].get('text').replace(' ', '').replace('₸', '').strip()

            # retail_price
            retail_price = list(filter(lambda item: 'Цена в магазинах сети' in item.get('title'), prices))
            if len(retail_price):
                product_dict['retail_price'] = retail_price[0].get('text').replace(' ', '').replace('₸', '').strip()

            # online_price
            online_price = list(filter(lambda item: 'Цена в интернет-магазине' in item.get('title'), prices))
            if len(online_price):
                product_dict['online_price'] = online_price[0].get('text').replace(' ', '').replace('₸', '').strip()

            # special_price
            special_price = list(filter(lambda item: 'Цена товара недели' in item.get('title'), prices))
            if len(special_price):
                product_dict['special_price'] = special_price[0].get('text').replace(' ', '').replace('₸', '').strip()

            # details
            details = []
            detail_elements = self.get_elements_by_selector(root, '.bx_detail_chars > .bx_detail_chars_i')

            for detail_element in detail_elements:
                title = self.get_element_by_selector(detail_element, '.bx_detail_chars_i_title')
                field = self.get_element_by_selector(detail_element, '.bx_detail_chars_i_field')
                if title is not None and field is not None:
                    details.append({'title': title.text_content(), 'field': field.text_content()})

            # uid
            uid = list(filter(lambda item: 'UID товара' in item.get('title'), details))
            if len(uid):
                product_dict['uid'] = uid[0].get('field').strip()

            # producer
            producer = list(filter(lambda item: 'Производитель' in item.get('title'), details))
            if len(producer):
                product_dict['producer'] = producer[0].get('field').strip()

            # model
            model = list(filter(lambda item: 'Модель' in item.get('title'), details))
            if len(model):
                product_dict['model'] = model[0].get('field').strip()
        except Exception as err:
            self.logger.warning(str(err))
        return product_dict
