import re
import sys
import scrapy
import logging
from urllib import parse

class MySpider(scrapy.Spider):
    def __new__(cls, *args, **kwargs):
        sys.stdout.reconfigure(encoding='utf-8')
        instance = super(MySpider, cls).__new__(cls, *args, **kwargs)
        return instance

    def start_requests(self):
        urls = [
            "https://www.cambridgenetwork.co.uk/companies/search-results",
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback,
                cb_kwargs={ "main_url": url }
        )

    def errback(self, failure):
        yield dict(
            main_url=failure.request.cb_kwargs["main_url"],
        )

    def parse(self, response, main_url):
        logger = logging.getLogger(__name__)
        selector = response.selector
        for companyitem in selector.xpath("//div[@class='views-row']/div[contains(@class, 'views-field-display-name-1')]/*[name()!='p']/a"):
            compname = re.sub(r'\W+','', companyitem.xpath('string()').get())
            compurl = companyitem.xpath('@href').get()
            logger.debug("Raw: %s", str(companyitem))
            logger.debug("Name: %s", str(companyitem.xpath('string()').get()))
            logger.debug("SanitName: %s", str(compname))
            logger.debug("Link: %s", str(compurl));

            # Click on the company link
            yield response.follow(
                compurl,
                self.parse2,
                cb_kwargs={
                    "company": compname,
                    "main_url": parse.urljoin(main_url, compurl)
                },
                errback=self.errback2,
            )

        for next_page in selector.xpath("//li[contains(@class, 'pager__item--next')]"):
            logger.debug("NP: %s", next_page)
#            yield response.follow(
#                next_page,
#                self.parse,
#                cb_kwargs={
#                    "main_url": parse.urljoin(main_url, compurl)
#                },
#                errback=self.errback,
#            )

    def errback2(self, failure):
        yield dict(
            main_url=failure.request.cb_kwargs["main_url"],
        )

    def parse2(self, response, main_url, company):
        logger = logging.getLogger(__name__)
        logger.debug("P2 for %s: %s", company, main_url)
#        yield { "name": companyitem.css('::text').get()}

    name = 'cbgnw'
