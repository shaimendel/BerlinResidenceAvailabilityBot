import os
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 800))  
display.start()

chromedriver_autoinstaller.install()

def send_to_telegram(text):
    apiToken = os.getenv("API_TOKEN")
    chatID = os.getenv("CHAT_ID")
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': text, 'parse_mode': 'MarkdownV2'})
        print(response.text)
    except Exception as e:
        print(e)


options = Options()
options.headless = True

# DRIVER_PATH_MAC = "/opt/homebrew/bin/chromedriver"
# driver = webdriver.Chrome(DRIVER_PATH_MAC, options=options)
driver = webdriver.Chrome(options=options)

def clickOnElement(by, text, message):
    sleep(4)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((by, text))).click()
    print(message)

try:
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.delete_all_cookies()
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })
    driver.get("https://www.berlin.de/einwanderung/dienstleistungen/service.871055.php/dienstleistung/305244/en/")
    clickOnElement(By.LINK_TEXT, "Make an appointment", "Clicked on make an apointment")
    clickOnElement(By.LINK_TEXT, "Book Appointment", "Clicked on book apointment")
    clickOnElement(By.XPATH, "//span[text()='I hereby declare that I have read and understood the information on this page. By using this service offer, I give my consent to the collection and use of my personal information.']", "Clicked on I declare")
    clickOnElement(By.ID, "applicationForm:managedForm:proceed", "Clicked next")

    sleep(10)
    clickOnElement(By.XPATH, "//select[@name='sel_staat']/option[text()='Israel']", "Chose Israel")
    clickOnElement(By.XPATH, "//select[@name='personenAnzahl_normal']/option[text()='one person']", "Chose to come alone")
    clickOnElement(By.XPATH, "//select[@name='lebnBrMitFmly']/option[text()='no']", "Chose I live alone")
    clickOnElement(By.XPATH, "//*[contains(text(), 'Apply for a residence title')]", "Chose Apply for a residenne title")
    clickOnElement(By.XPATH, "//*[contains(text(), 'Educational purposes')]", "Chose educational purposes")
    clickOnElement(By.XPATH, "//*[contains(text(), 'Residence permit to take part in a student exchange')]", "Chose student exchange")
    clickOnElement(By.ID, "applicationForm:managedForm:proceed", "Clicked next")

    try:
        print("Waiting for dates page")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'There are currently no dates available for the selected service')]")))
        send_to_telegram("No dates available yet \U0001f62d")
    except:
        send_to_telegram("\U0001f389 *Found dates\\!* \U0001f389 Go check at [the website](https://www.berlin.de/einwanderung/dienstleistungen/service.871055.php/dienstleistung/305244/en/)")

finally:
    try:
        driver.close()
    except:
        pass
