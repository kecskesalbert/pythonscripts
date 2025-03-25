import re
import sys
import scrapy
import logging
from urllib import parse

class MySpider(scrapy.Spider):
    name = 'cbgnw'

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

    # TODO: get error code/message
    def errback(self, failure):
        yield dict(
            main_url=failure.request.cb_kwargs["main_url"],
        )

    # List of companies page
    def parse(self, response, main_url):
        logger = logging.getLogger(__name__)
        selector = response.selector
        for companyitem in selector.xpath("//div[@class='views-row']/div[contains(@class, 'views-field-display-name-1')]/*[name()!='p']/a"):
            company_name = re.sub(r'\W+','', companyitem.xpath('string()').get())
            company_url = companyitem.xpath('@href').get()

            # Click on the company link
            yield response.follow(
                company_url,
                self.parse2,
                cb_kwargs={
                    "company_name": company_name,
                    "main_url": parse.urljoin(main_url, company_url)
                },
                errback=self.errback,
            )

        # Go to next page
        for next_page in selector.xpath("//li[contains(@class, 'pager__item--next')]"):
            nplink = next_page.xpath('./*[1]').xpath('@href').get()
            yield response.follow(
                nplink,
                self.parse,
                cb_kwargs={
                    "main_url": parse.urljoin(main_url, company_url)
                },
                errback=self.errback,
            )

    # Company showcase page
    def parse2(self, response, main_url, company_name):
        logger = logging.getLogger(__name__)
        found = dict(
            name=company_name,
            address="",
            webpage="",
            size="",
        )
        for detail in response.selector.xpath("//div[contains(@class, 'article-aside')]//div[contains(@class, 'views-row')]"):
            childcount = int(float(detail.xpath("count(./*)").get()))
            if (childcount == 5):
                addrpiece = []
                for piece in detail.xpath("./*"):
                    ptext = piece.xpath('string()').get()
                    if (ptext):
                        addrpiece.append(ptext)
                found["address"] = ", ".join(addrpiece)
                continue
            fc = detail.xpath("./*[1]")
            if (childcount == 1 and
                fc.xpath("name(.)").get() == "a" and
                found["webpage"] == ""):
                found['webpage'] = fc.xpath("@href").get()
                continue
            found['size'] = detail.xpath('string()').get()
        yield found

    # end of class MySpider

sys.stdout.reconfigure(encoding='utf-8')
