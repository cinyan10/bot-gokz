import os
from datetime import datetime, timedelta

from selenium import webdriver
from PIL import Image
from io import BytesIO
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait

from config import RESOURCE_URL
from utils.file_operation.file_operation import check_last_modified_date
from utils.globalapi.kz_mode import format_kzmode_simple
from utils.steam.steam import convert_steamid

LOCAL_PATH = "/www/wwwroot/fastdl.axekz.com/images/"

LOCAL_AUDIO_PATH = "/www/wwwroot/fastdl.axekz.com/audio/"

executor = ThreadPoolExecutor(max_workers=5)


async def kzgoeu_screenshot_async(steamid, kz_mode, force_update=False):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, kzgoeu_screenshot, steamid, kz_mode, force_update
    )
    return result


async def kzgoeu_compare_screenshot_async(steamid1, steamid2, kz_mode):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, kzgoeu_compare_screenshot, steamid1, steamid2, kz_mode
    )
    return result


async def vnl_screenshot_async(steamid):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, vnl_screenshot, steamid)
    return result


def kzgoeu_screenshot(steamid, kz_mode, force_update=False):
    steamid = convert_steamid(steamid)
    kz_mode = format_kzmode_simple(kz_mode)

    image_url = f"kzgo/{steamid}_{kz_mode}.png"

    # Check last modified date of the file
    filepath = os.path.join(LOCAL_PATH, image_url)
    last_modified_date = check_last_modified_date(filepath)

    if not force_update:
        if last_modified_date and (
            datetime.now() - last_modified_date <= timedelta(days=1)
        ):
            # If file modified within 1 day, return URL directly
            return image_url

    # 使用Selenium打开浏览器
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # 无头模式，无需图形界面
    options.add_argument("--lang=zh_CN")
    options.add_argument('--font-family="WenQuanYi Zen Hei"')

    driver = webdriver.Firefox(
        options=options
    )  # 使用Firefox浏览器，无需安装额外驱动程序

    # 打开网页
    kzgo_url = f"https://kzgo.eu/players/{steamid}?{kz_mode}"
    driver.get(kzgo_url)

    # 设置浏览器窗口大小
    width = 700
    height = 1000
    driver.set_window_size(width, height)

    # 等待网页加载完成
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "progress-bg")))
    time.sleep(1)

    # 截取整个网页的截图
    screenshot = driver.get_screenshot_as_png()

    # 关闭浏览器
    driver.quit()

    # 使用Pillow打开截图
    img = Image.open(BytesIO(screenshot))

    # 裁剪图片
    left = 90
    top = 100

    right = width - 100
    bottom = height - 280

    cropped_img = img.crop((left, top, right, bottom))

    # 保存截图到文件
    cropped_img.save(LOCAL_PATH + image_url)

    return image_url


def kzgoeu_compare_screenshot(steamid1, steamid2, kz_mode):
    kz_mode = format_kzmode_simple(kz_mode)
    url = f"kzgo/{steamid1}vs{steamid2}_{kz_mode}.png"

    # 使用Selenium打开浏览器
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # 无头模式，无需图形界面
    options.add_argument("--lang=zh_CN")
    options.add_argument('--font-family="WenQuanYi Zen Hei"')

    filepath = os.path.join(LOCAL_PATH, url)
    last_modified_date = check_last_modified_date(filepath)

    if last_modified_date and (
        datetime.now() - last_modified_date <= timedelta(days=1)
    ):
        return url

    driver = webdriver.Firefox(
        options=options
    )  # 使用Firefox浏览器，无需安装额外驱动程序

    # 打开网页
    kzgo_compare_url = (
        f"https://kzgo.eu/compare?player1={steamid1}&player2={steamid2}&{kz_mode}"
    )
    driver.get(kzgo_compare_url)

    # 设置浏览器窗口大小
    width = 1200
    height = 1000
    driver.set_window_size(width, height)

    # 等待网页加载完成
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "progress-bg")))

    # 截取整个网页的截图
    screenshot1 = driver.get_screenshot_as_png()

    # 使用Pillow打开截图
    image1 = Image.open(BytesIO(screenshot1))

    # 裁剪图片
    left = 0
    top = 90
    right = width
    bottom = height

    image1 = image1.crop((left, top, right, bottom))

    # 获取Pro对比
    element = driver.find_element(By.CSS_SELECTOR, ".pro")
    element.click()

    time.sleep(5)

    screenshot2 = driver.get_screenshot_as_png()

    driver.quit()

    # 使用Pillow打开截图
    image2 = Image.open(BytesIO(screenshot2))

    # 裁剪图片
    left = 0
    top = 240
    right = width
    bottom = height

    image2 = image2.crop((left, top, right, bottom))

    width1, height1 = image1.size
    width2, height2 = image2.size

    # 确保两张图片的宽度相同
    if width1 != width2:
        raise ValueError("图片宽度不一致")

    # 创建一个新的图片，宽度不变，高度为两张图片高度之和
    new_image = Image.new("RGB", (width1, height1 + height2 - 180))

    # 将两张图片粘贴到新的图片上
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (0, height1 - 90))

    # 保存拼接后的图片
    new_image.save(LOCAL_PATH + url)

    return kzgo_compare_url


def vnl_screenshot(steamid):
    steamid64 = convert_steamid(steamid, 2)
    steamid = convert_steamid(steamid)

    image_url = f"kzgo/{steamid}_vnl.png"

    # 检查文件的最后修改日期, 小于1天直接返回url
    filepath = os.path.join(LOCAL_PATH, image_url)
    last_modified_date = check_last_modified_date(filepath)
    if last_modified_date and (
        datetime.now() - last_modified_date <= timedelta(days=1)
    ):
        return image_url

    # 使用Selenium打开浏览器
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # 无头模式，无需图形界面
    options.add_argument("--lang=zh_CN")
    options.add_argument('--font-family="WenQuanYi Zen Hei"')

    driver = webdriver.Firefox(options=options)

    kzgo_url = f"https://vnl.kz/#/stats/{steamid64}"
    driver.get(kzgo_url)

    # 设置浏览器窗口大小
    width = 840
    height = 620
    driver.set_window_size(width, height)

    # 等待网页加载完成
    time.sleep(15)

    # 截取整个网页的截图
    screenshot = driver.get_screenshot_as_png()

    # 关闭浏览器
    driver.quit()

    # 使用Pillow打开截图
    img = Image.open(BytesIO(screenshot))

    # 裁剪图片
    left = 0
    top = 60

    right = width - 15
    bottom = height - 75

    cropped_img = img.crop((left, top, right, bottom))

    # 保存截图到文件
    cropped_img.save(LOCAL_PATH + image_url)

    return image_url


if __name__ == "__main__":
    url = kzgoeu_screenshot("STEAM_1:0:219021707", "kzt", True)
    print(RESOURCE_URL + "images/" + url)
