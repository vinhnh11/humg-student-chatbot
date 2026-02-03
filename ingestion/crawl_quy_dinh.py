import asyncio
import requests
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from config.settings import MAIN_URL, API_LOC_QUYDINH, PDF_DIR

CLICK_WAIT = 2000


async def get_all_ids():
    ids = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        async def handle_response(response):
            if "w-locdsquydinh" in response.url:
                try:
                    data = await response.json()
                    item = data.get("data", {}).get("quy_dinh", {})
                    if item and "id" in item:
                        ids.add(item["id"])
                        print("📡 Bắt được ID:", item["id"])
                except:
                    pass

        page.on("response", handle_response)

        await page.goto(MAIN_URL)
        await page.wait_for_timeout(50000)

        try:
            await page.click("li.el-menu-item:has-text('Quy chế – Quy định')")
            await page.wait_for_timeout(CLICK_WAIT)
        except:
            pass

        items = await page.query_selector_all("li.el-menu-item")
        total = len(items)
        print(f"Tổng số mục con tìm được: {total}")

        for i in range(total):
            items = await page.query_selector_all("li.el-menu-item")
            try:
                print(f"➡ Click mục {i + 1}/{total}")
                await items[i].click()
                await page.wait_for_timeout(CLICK_WAIT)
            except:
                print("Click lỗi mục", i + 1)

        await browser.close()

    return list(ids)


def download_pdfs(ids):
    headers = {"Content-Type": "application/json"}

    for id_ in ids:
        payload = {"filter": {"id": id_}}

        try:
            res = requests.post(API_LOC_QUYDINH, headers=headers, json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f"Lỗi lấy nội dung ID {id_}: {e}")
            continue

        html_content = data.get("data", {}).get("quy_dinh", {}).get("noi_dung", "")
        if not html_content:
            continue

        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            pdf_url = link.get("href")
            if not pdf_url:
                continue

            if not pdf_url.startswith("http"):
                pdf_url = MAIN_URL + pdf_url

            filename = pdf_url.split("/")[-1]
            filepath = PDF_DIR / filename   # ✅ CHUẨN

            if filepath.exists():
                print(f"⏭ Đã tồn tại, bỏ qua: {filename}")
                continue

            try:
                response = requests.get(pdf_url, timeout=15)
                response.raise_for_status()

                with open(filepath, "wb") as f:
                    f.write(response.content)

                print(f"⬇ Đã tải: {filename}")

            except Exception as e:
                print(f"Lỗi tải {pdf_url}: {e}")


async def main():
    print("BẮT ĐẦU QUÉT TẤT CẢ QUY CHẾ...\n")
    ids = await get_all_ids()

    if not ids:
        print("Không lấy được ID nào.")
        return

    print(f"\nTổng số ID: {len(ids)}")
    download_pdfs(ids)
    print("\nHOÀN TẤT!")


if __name__ == "__main__":
    asyncio.run(main())
