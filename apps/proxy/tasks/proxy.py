# import random

from celery import shared_task

from ..models import Country, Proxy
from ..parsers import ProxyParser


@shared_task(bind=True, max_retries=3)
def proxy_task(self, country_id=None):
    """Proxy task"""
    try:
        country = Country.objects.get(id=country_id)
        country.status = Country.STATUS_CHOICE_ERROR
        country.save()

        # proxy parser
        proxy_parser = ProxyParser()

        # proxy
        # proxy_list = [proxy.value for proxy in Proxy.objects.filter(is_active=True, type=Proxy.TYPE_CHOICE_HTTPS)]
        #
        # if len(proxy_list):
        #     proxy_server = random.choice(proxy_list)
        # else:
        #     proxy_server = None

        proxies = proxy_parser.parse_proxy(country_link=country.link, proxy_server=None)

        for proxy in proxies:
            if proxy.get('type') == 'HTTP':
                proxy_type = Proxy.TYPE_CHOICE_HTTP
            elif proxy.get('type') == 'HTTPS':
                proxy_type = Proxy.TYPE_CHOICE_HTTPS
            elif proxy.get('type') == 'SOCK5':
                proxy_type = Proxy.TYPE_CHOICE_SOCK5
            else:
                proxy_type = Proxy.TYPE_CHOICE_NONE

            Proxy.objects.get_or_create(value=proxy.get('value'),
                                        country=country,
                                        defaults={'type': proxy_type, 'latency': 1})

        country.status = Country.STATUS_CHOICE_DONE
        country.save()
    except Country.DoesNotExist as err:
        pass
    except Exception as err:
        self.retry(countdown=30)
