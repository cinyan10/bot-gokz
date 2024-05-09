import datetime
import os
import asyncio
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

from config import LOCAL_PATH

executor = ThreadPoolExecutor(max_workers=1)


async def take_screenshot():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, capture_screenshot)
    return result


def capture_screenshot():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model

    driver = webdriver.Chrome(options=options)

    url = "https://www.axekz.com/servers"
    driver.get(url)

    width = 1920
    height = 1080
    driver.set_window_size(width, height)

    # Update this path as needed
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    img = Image.open(BytesIO(screenshot))

    left = 285
    top = 121

    right = width - 285
    bottom = height - 150

    cropped_img = img.crop((left, top, right, bottom))

    # 保存截图到文件
    screenshot_path = f"{LOCAL_PATH}servers.png"
    cropped_img.save(screenshot_path)

    return "servers.png"


# Usage
if __name__ == "__main__":
    screenshot_url = asyncio.run(take_screenshot())
    print(screenshot_url)
    # print(datetime.datetime.now())
