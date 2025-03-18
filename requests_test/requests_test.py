#!/usr/bin/env python

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

class parser_greenhouse:
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
                print('Found:', repr(link_tag.contents[0]),
                    'at:', repr(location_tag.contents[0]),
                    'in department:', repr(department_name),
                    'link:', repr(link_tag['href']),
                )

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

            ret['html'] = fetch_response.text
        except requests.exceptions.RequestException as err:
            return({'err': err})

    parser = parser_class()
    ret = parser.parse(ret['html'])
    return(ret)

def main():
    crawl_list = [
    ('https://boards.eu.greenhouse.io/darktracelimited', None, parser_greenhouse),
    ('https://boards.greenhouse.io/graphcore', None, parser_greenhouse),
    ('https://www.speechmatics.com/company/careers/roles', None, parser_speechmatics),
    ]

    for params in crawl_list:
        resp = fetchpage(params[0],params[1],params[2])
        # print(resp)

if __name__ == "__main__":
    # This is required utf-8 for printing utf8 to stdout, probably on Windows only
    sys.stdout.reconfigure(encoding='utf-8')
    main()
