# /usr/bin/env python

import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup, SoupStrainer
import json

import sys


def printtag(tag, depth=0):
    print(
        "  " * depth,
        tag.name,
        type(tag), 
        str(len(tag.attrs)) + ' attrs,' if hasattr(tag, 'attrs') else '', 
        str(len(tag.contents)) + ' children' if hasattr(tag, 'contents') else '',
        repr(str(tag)[:20].strip())
    )
    if hasattr(tag, 'attrs'):
        for attr in tag.attrs.keys():
            print("  " * depth, " -", attr, repr(str(tag.attrs[attr])[:30]).strip())
    if hasattr(tag, 'contents'):
        for child in tag.contents:
            printtag(child, depth+1)
    
class parser_stub:
    def __init__(self):
        pass
    def parse(self, html, params=None):
        soup = BeautifulSoup(html, 'html.parser')
        printtag(soup)

class parser_speechmatics:
    def __init__(self):
        pass
    def parse(self, html, params=None):
        soup = BeautifulSoup(html, 'html.parser')
        jobs_json = soup.find('script', attrs = {'id':'__NEXT_DATA__', 'type':'application/json'})
        json_content = json.loads(jobs_json.contents[0])
        for item in json_content['props']['pageProps']['page']['blocksCollection']['items']:
            if item['__typename'] != 'BlockAvailableRoles':
                continue
            for department in item['rolesByDepartment']:
                for job in department['jobs']:
                    print('Found:', job['title'],
                        'at:', job['location']['name'],
                        'in department:',department['name'],
                        'last_updated:', job['updated_at'],
                        'link:', job['absolute_url'],
                    )

class parser_darktrace:
    def __init__(self):
        pass
    def parse(self, html, params=None):
        soup = BeautifulSoup(html, 'html.parser')
        for department in soup.find_all(name = 'section', attrs = {'class': 'level-0'}):
            department_name = department.find(name='h3').contents[0]
            for job in department.find_all(name='div', attrs = {'class': 'opening'}):
                link_tag = job.find(name='a')
                if link_tag is None:
                    continue
                location_tag = job.find(name='span', attrs = {'class': 'location'})
                if location_tag is None:
                    continue                
                print('Found:', link_tag.contents[0],
                    'at:', location_tag.contents[0],
                    'in department:', department_name,
                    'link:', link_tag['href'],
                )

# In: 
# url: page URL as string
# request_args: request arguments as dict
# parser_class: classname of parser
def fetchpage(url, request_args, parser_class):
    ret = {'html': None}
    parts = url.split('://',2)
    if (len(parts)==2 and parts[0]=='file'):
        f = open(parts[1], "r")
        ret['html'] = f.read()
        f.close()
        ret['source']='file'
    else:
        print("GET", repr(url[:75]))
        try:
            fetch_response = requests.get(
                url,
                request_args,
            )

            # Raise HTTPError for http errors
            fetch_response.raise_for_status()

# Non-blocking :
# https://dev.to/sagnew/asynchronous-http-requests-in-python-with-httpx-and-asyncio-2n19
# https://stackoverflow.com/questions/67713274/python-asyncio-httpx
# https://requests.readthedocs.io/en/latest/user/advanced/#blocking-or-non-blocking
# https://www.zenrows.com/blog/python-parallel-requests
# https://towardsdev.com/multithreaded-http-requests-in-python-453f07db98e1
# https://stackoverflow.com/questions/9110593/asynchronous-requests-with-python-requests
# http://web.archive.org/web/20071001004937/http://members.verizon.net/olsongt/stackless/why_stackless.html#why-stackless

    # .url
    # .headers: headers
    # .content: content as bytes
    # .text:    content as string
    # .json():  content as json

            ret['html'] = fetch_response.text
        except requests.exceptions.RequestException as err:
            return({'err': err})        

    parser = parser_class()
    ret = parser.parse(ret['html'])
    return(ret)


# if __name__ == "__main__":

for params in [
    ('https://boards.eu.greenhouse.io/darktracelimited',None,parser_darktrace),
    ('https://www.speechmatics.com/company/careers/roles', { 'timeout': (5,2) }, parser_speechmatics),
    
    ]:
    resp = fetchpage(params[0],params[1],params[2])
    # print(resp)


