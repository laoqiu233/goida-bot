import asyncio

import feedparser
import httpx
import playwright
from pgpt_python.client import AsyncPrivateGPTApi
from playwright.async_api import async_playwright

rss_source = "https://lenta.ru/rss"

pgpt_client = AsyncPrivateGPTApi(base_url="http://localhost:8001")


async def main():
    health_response = await pgpt_client.health.health()
    print(health_response.json())

    async with httpx.AsyncClient() as client:
        resp = await client.get(rss_source)

    rss = feedparser.parse(resp.text)

    for entry in rss.entries[:10]:
        uid = entry.link.removesuffix("/").split("/")[-1]
        print(f"Downloading {entry.title} {uid}")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            response = await page.goto(entry.link)

            if response is None:
                print(f"no response for {uid}")
                continue

            if response.ok:
                result = await page.pdf()
                with open(f"content/{uid}.pdf", "wb") as file:
                    file.write(result)

                print(f"{uid} downloaded, embedding...")

                with open(f"content/{uid}.pdf", "rb") as file:
                    embed_response = await pgpt_client.ingestion.ingest_file(file=file)
                    print(f"Embedding finished: {embed_response}")
            else:
                print(f"failed with {response.status}: {resp.text}")

        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
