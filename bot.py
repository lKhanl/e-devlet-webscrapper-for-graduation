import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
from dotenv import load_dotenv
from mail_send import send_mail
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

def main():

    WINDOW_SIZE = "1920,1080"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://giris.turkiye.gov.tr/Giris/gir")
    

    tc = driver.find_element(By.ID, "tridField")
    password = driver.find_element(By.ID, "egpField")
    login_button = driver.find_element(By.NAME, "submitButton")

    tc_value = os.environ.get("tc")
    password_value = os.environ.get("e_password")
    tc.send_keys(tc_value)
    password.send_keys(password_value)
    login_button.click()

    driver.get("https://www.turkiye.gov.tr/yuksekogretim-mezun-belgesi-sorgulama")

    time.sleep(30)

    try:
        driver.find_element(By.CLASS_NAME, "warningContainer").text
    except:
        subject = "Mezuniyet Belgesi Durumu"
        message = "Tebrikler, Mezun Oldunuz!"
        send_mail(os.environ.get("from_mail"), os.environ.get("mail_password"), os.environ.get("to_mail"), subject, message)

    driver.close()

if __name__ == "__main__":
    main()

