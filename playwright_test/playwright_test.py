#!/usr/bin/env python

import asyncio
from playwright.async_api import async_playwright, expect
import re
import sys

async def runtest():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(50000)
        await page.goto("https://sec.wd3.myworkdayjobs.com/Samsung_Careers?locations=490fb96c8f12100dcd6b4d958d150000")
        # await page.goto("https://sec.wd3.myworkdayjobs.com/Samsung_Careers")

        page_number = 1
        while True:
            await page.title()
            await page.content()

            jobfooter_locator = page.locator('p[data-automation-id="jobOutOfText"]')
            await expect(jobfooter_locator).to_have_text(re.compile(r"^\s*(\d+)\s+-\s+(\d+)\s+of\s+(\d+)\s+jobs"))
            jobfooter_text = await jobfooter_locator.first.all_text_contents()
            print(f"Page {page_number}: {jobfooter_text[0]}")
            footer_match = re.match(r"^\s*(\d+)\s+-\s+(\d+)\s+of\s+(\d+)\s+jobs", jobfooter_text[0])
            if (not footer_match):
                raise Exception(f"Text not recognized: {jobfooter_text[0]}")

            every_title = await page.locator('a[data-automation-id="jobTitle"]').all()
            print("Title", len(every_title))
            every_remote = await page.locator('div[data-automation-id="remoteType"]').all()
            print("Remote", len(every_remote))
            every_posted = await page.locator('div[ data-automation-id="postedOn"]').all()
            print("Posted", len(every_posted))
            every_ref = await page.locator('ul[data-automation-id="subtitle"]').all()
            print("Ref", len(every_ref))

            if (
                int(footer_match.groups()[1]) - int(footer_match.groups()[0]) + 1 != len(every_title) or
                len(every_title) != len(every_remote) or
                len(every_remote) != len(every_posted) or
                len(every_posted) != len(every_ref)
            ):
                raise Exception("Unrecognized metadata")

            # TODO: Only the first job is captured
            for jobitem in range(len(every_title)):
                print(await every_title[jobitem].get_attribute(name="href"))
                await every_title[jobitem].click()
                await page.wait_for_load_state("networkidle")
                html = await page.content()
                f = open(f"job-{jobitem}.html", "w", encoding='utf-8')
                f.write(html)
                f.close()
                await page.screenshot(path=f"job{jobitem}.png", full_page=True);
                await page.locator('button[data-automation-id="jobDetailsCloseButton"]').nth(0).click()
                await page.wait_for_load_state("networkidle")

            html = await page.content()
            f = open(f"out-page-{page_number}.html", "w", encoding='utf-8')
            f.write(html)
            f.close()

            # Exit the loop when we have the last item
            if (int(footer_match.groups()[1]) >= int(footer_match.groups()[2])):
                break

            # Otherwise press the "Next page" button
            page_number += 1
            await page.get_by_label("next").click()
        await browser.close()

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(runtest())
