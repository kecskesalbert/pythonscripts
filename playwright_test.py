#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright, expect
import re

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

            html = await page.content()
            f = open(f"out-page-{page_number}.html", "w", encoding='utf-8')
            f.write(html)
            f.close()
            # await page.screenshot(path='playwright_test.png', full_page=True);

            # Exit the loop when we have the last item
            if (int(footer_match.groups()[1]) >= int(footer_match.groups()[2])):
                break

            # Otherwise press the "Next page" button
            page_number += 1
            await page.get_by_label("next").click()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(runtest())

# Title + link
# <a aria-current="false" data-automation-id="jobTitle" data-uxi-element-id="jobItem" data-uxi-query-id="" data-uxi-widget-type="heading" data-uxi-item-rank="6" class="css-19uc56f" href="/en-US/Samsung_Careers/job/6-rue-Fructidor-Saint-Ouen-France/Alternance-Business-Analyst-Finance---H-F---1-an_R99441">Alternance Business Analyst Finance, (H/F) â€“1 an</a>

# Remote type
# <div class="css-248241"><div class="css-1y87fhn"><div data-automation-id="remoteType" class="css-k008qs">

# Posted on
#<div data-automation-id="postedOn" class="css-k008qs">

# Reference
# <ul data-automation-id="subtitle" class="css-14a0imc">


