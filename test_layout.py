import asyncio

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=True)
        page = await browser.new_page()
        # Ensure django server is running or we just load a simple HTML with the exact CSS

        # Or even better, let's just create a minimal HTML file with the form to test the rendering.
        # But maybe we should just go to the local dev server.
        # We will assume the dev server is running on port 8000.
        try:
            await page.goto("http://127.0.0.1:8000/")
            await page.wait_for_timeout(1000)  # Give it a moment to load font
            await page.screenshot(path="screenshot.png")
            print("Screenshot saved to screenshot.png")
        except Exception as e:
            print(f"Failed to connect to dev server: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
