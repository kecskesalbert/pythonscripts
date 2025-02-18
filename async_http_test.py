#!/usr/bin/env python

# Read the list of local companies published on cambridgenetwork.co.uk
# Output them as semicolon separeated csv: name, webpage, address, size

# TODO:
# Catch random httpx.ReadTimeout exceptions, retry
# Limit concurrency, take argument as parameter
# async follow redirects
# use csv module for flexible output
# Take timeout as parameter

import asyncio
import httpx
from bs4 import BeautifulSoup, SoupStrainer
import lxml
import re
import sys
#from urllib.parse import urljoin
from urllib import parse

async def fetchpage(base_url='https://www.cambridgenetwork.co.uk/companies/search-results'):
    async with httpx.AsyncClient() as httpx_client:
        for prefix in ([0,] + list(range(65,91))):
        #for prefix in (range(67,70)):
            page_number = 0
            url = base_url + "?" + parse.urlencode({True:{'numeric': 1}, False: {'prefix': chr(prefix)}}[prefix==0])
            while True:
                print("REQ", str(url)[:75], file=sys.stderr)
                resp = await httpx_client.get(url, follow_redirects=True)
                print("RSP", str(resp.url)[:75], resp.status_code, flush=False, file=sys.stderr)
                lentilsoup = BeautifulSoup(resp.text, 'lxml')

                # List of companies
                for companyitem in lentilsoup.find_all(name='div', class_='views-row'):
                    found = { "address": "", "webpage": "", "size": "", "name": "" }
                    companydiv = companyitem.find(name='div', class_= 'views-field-display-name-1').contents[0].contents[0]
                    url = parse.urljoin(base_url, companydiv['href'])
                    found["name"] = re.sub(r'\W+','', companydiv.string)

                    # Company showcase page
                    print("REQ", url[:75], file=sys.stderr)
                    resp = await httpx_client.get(url, follow_redirects=True)
                    print("RSP", str(resp.url)[:75], resp.status_code, flush=True, file=sys.stderr)
                    carrotsoup = BeautifulSoup(resp.text, 'lxml')

                    for detailitem in carrotsoup.find(name='div', class_='article-aside').find_all(name='div', class_='views-row'):
                        #print("\n>>>")
                        #print(len(detailitem.contents), detailitem.contents)
                        #print("<<<\n")
                        if (len(detailitem.contents) == 5):
                            for piece in detailitem.contents:
                                if (piece.string is None):
                                    continue
                                found["address"] = \
                                {True: "", False: found["address"] + ", "}[len(found["address"])==0] + \
                                {True: "", False: str(piece.string)}[piece.string is None]
                            continue
                        if (len(detailitem.contents) != 1):
                            continue
                        if (detailitem.contents[0].name == 'a'):
                            if (found["webpage"] == ""):
                                found['webpage'] = detailitem.contents[0]['href']
                        else:
                            found['size'] = detailitem.contents[0].string

                    print(";".join((found["name"], found["webpage"], found["address"], found["size"])), flush=False)

                # Next page button
                next_page = (lentilsoup.find_all(name='li', attrs = {'class': 'pager__item pager__item--next'}, limit=1))
                if len(next_page) == 0:
                    break
                url = parse.urljoin(base_url, next_page[0].find(name='a')['href'])


def main():
    # This is required utf-8 for printing utf8 to stdout, probably only on Windows
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(fetchpage())

if __name__ == "__main__":
    main()
