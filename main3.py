from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import time
from PIL import Image
import cv2


SELENIUM_SESSION_FILE = './selenium_session'
SELENIUM_PORT=9515

def build_driver():
    options = ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--enable-file-cookies")

    if os.path.isfile(SELENIUM_SESSION_FILE):
        session_file = open(SELENIUM_SESSION_FILE)
        session_info = session_file.readlines()
        session_file.close()

        executor_url = session_info[0].strip()
        session_id = session_info[1].strip()

        capabilities = options.to_capabilities()
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
        # prevent annoying empty chrome windows
        driver.close()
        driver.quit()

        # attach to existing session
        driver.session_id = session_id
        return driver

    driver = Chrome(options=options)

    session_file = open(SELENIUM_SESSION_FILE, 'w')
    session_file.writelines([
        driver.command_executor._url,
        "\n",
        driver.session_id,
        "\n",
    ])
    session_file.close()

    return driver

driver = build_driver()
driver.get("https://google.com/")
url = "https://breached.vc/"
driver.get(url)
driver.find_element(By.CLASS_NAME, "panel__module--login").click()

while True:
    print(driver.current_url)
    if "index" not in driver.current_url:
        break

    username_field = driver.find_element(By.NAME, "username").send_keys("afit_akbar")
    password_field = driver.find_element(By.NAME, "password").send_keys("Akbar123")
    captcha_img = driver.find_element(By.ID, "captcha_img")
    captcha_img_loc = captcha_img.location
    captcha_img_size = captcha_img.size

    driver.save_screenshot("screenshot.png")
    x = captcha_img_loc['x']
    y = captcha_img_loc['y']
    w = captcha_img_size['width']
    h = captcha_img_size['height']
    width = x + w
    height = y + h

    im = Image.open('screenshot.png')
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save('captcha.png')

    import cv2
    import pytesseract
    import numpy as np
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    img = cv2.imread("captcha.png")

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ekernel = np.ones((1,2),np.uint8)
    # eroded = cv2.erode(gray, ekernel, iterations = 1)
    # dkernel = np.ones((2,3),np.uint8)
    # dilated_once = cv2.dilate(eroded, dkernel, iterations = 1)
    # ekernel = np.ones((2,2),np.uint8)
    # dilated_twice = cv2.erode(dilated_once, ekernel, iterations = 1)
    # th, threshed = cv2.threshold(dilated_twice, 200, 255, cv2.THRESH_BINARY)
    # dkernel = np.ones((2,2),np.uint8)
    # threshed_dilated = cv2.dilate(threshed, dkernel, iterations = 1)
    # ekernel = np.ones((2,2),np.uint8)
    # thr = cv2.erode(threshed_dilated, ekernel, iterations = 1)

    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = gry.shape[:2]
    gry = cv2.resize(gry, (w*2, h*2))
    cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
    thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    txt = pytesseract.image_to_string(thr)
    captcha = str(txt).replace(" ", "").strip()
    # print(captcha)

    captcha_field = driver.find_element(By.NAME, "imagestring").send_keys(captcha)

    login_button = driver.find_element(By.NAME, "submit").click()




time.sleep(1000)