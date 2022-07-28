##
# Author  : Sandroputraa
# Name    : WhatsApp Main Class - WhatsApp Blaster
# Build   : 28-07-2022
#
# If you are a reliable programmer or the best developer, please don't change anything.
# If you want to be appreciated by others, then don't change anything in this script.
# Please respect me for making this tool from the beginning.
##

import os
import json
from os.path import exists

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import JavascriptException


class WhatsappMain:

    def __init__(self):

        self.url = 'https://web.whatsapp.com/'
        self.executor = 'http://127.0.0.1:4444/wd/hub'

        with open(os.path.join(os.getcwd(), "src", "session_id"), "w") as script:
            script.write('')

        with open(os.path.join(os.getcwd(), "src", "session_id"), "r") as script:
            self.session = script.read()

    def ConnectDriver(self):
        from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute
        session_id = self.session

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(command_executor=self.executor, desired_capabilities={})
        new_driver.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        return new_driver

    def build_driver(self):
        global binary_path

        if exists("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"):
            binary_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        elif exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"):
            binary_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        else:
            print("Chrome Browser not found")
            exit()

        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--ignore-certificate-errors')
        options.binary_location = binary_path
        options.add_argument(
            "user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        desiredCapabilities = {
            "browserName": "chrome"
        }

        driver = webdriver.Remote(command_executor=self.executor,
                                  desired_capabilities=desiredCapabilities, options=options)
        driver.get(self.url)
        self.session = driver.session_id
        with open(os.path.join(os.getcwd(), "src", "session_id"), "w") as script:
            script.write(self.session)

        return driver

    def scan_qr(self):
        driver = self.ConnectDriver()
        try:

            qr = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='qrcode']")))
            qr.screenshot('qr.png')
            return True
        except TimeoutException:
            return False

    def check_whatsapp_logedin(self):

        if self.session == '':
            return False

        try:
            driver = self.ConnectDriver()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list-search']")))
            try:

                script_path = os.getcwd()
                with open(os.path.join(script_path, "src", "wapi.js"), "rb") as script:
                    driver.execute_script(script.read().decode('utf-8'))

                driver.execute_script("return window.WAPI").keys()
            except JavascriptException as e:
                pass

            return True
        except TimeoutException:
            return False

    def send_message(self, id, message):
        driver = self.ConnectDriver()

        if "@c.us" in id:
            id = id
        else:
            id = str(id) + "@c.us"
        try:
            print("[~] Sending message to " + id)
            driver.execute_script("return window.WAPI.sendMessage('" + str(id) + "','" + message + "')")
            return True
        except JavascriptException as e:
            return False

    def check_browser_running(self):
        try:
            driver = self.ConnectDriver()
            driver.title
            return True
        except:
            return False

    def info_loggedin(self):
        driver = self.ConnectDriver()
        try:
            image = driver.execute_script(
                "return Store.Contact.get(localStorage['last-wid-md'].slice(1, -9) + '@c.us')['__x_profilePicThumb']['__x_imgFull'];");
            display_name = driver.execute_script(
                "return Store.Contact.get(localStorage['last-wid-md'].slice(1, -9) + '@c.us')['__x_displayName'];");
            phone_number = driver.execute_script(
                "return Store.Contact.get(localStorage['last-wid-md'].slice(1, -9) + '@c.us')['__x_formattedUser'];");
            return {'image': image, 'display_name': display_name, 'phone_number': phone_number}
        except JavascriptException as e:
            image = driver.execute_script(
                "return  Store.Contact.find(localStorage['last-wid-md'].slice(1, -5).split(':')[0] + '@c.us')['_value']['__x_profilePicThumb']['__x_imgFull'];");
            display_name = driver.execute_script(
                "return  Store.Contact.find(localStorage['last-wid-md'].slice(1, -5).split(':')[0] + '@c.us')['_value']['__x_displayName'];");
            phone_number = driver.execute_script(
                "return  Store.Contact.find(localStorage['last-wid-md'].slice(1, -5).split(':')[0] + '@c.us')['_value']['__x_formattedUser'];");
            return {'image': image, 'display_name': display_name, 'phone_number': phone_number}

    def get_all_contact(self):
        driver = self.ConnectDriver()
        contact = driver.execute_script("return window.WAPI.getAllContacts()")
        json_object = json.dumps(contact)
        with open("src/contact.json", "w", encoding="utf-8") as outfile:
            outfile.write(json_object)

        f = open("src/contact.json", encoding="utf8")
        contact = []
        data = json.load(f)
        for i in range(len(data)):
            contact.append(data[i]['formattedName'] + '|' + data[i]['id'])
        return contact
