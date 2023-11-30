import time
import typing

import requests
from faker import Faker
from bs4 import BeautifulSoup

from core import paths
from core.logger import logger


class GetimgReger:
    DEFAULT_PASSWORD = "qwe123QWE!@#"
    
    HEADERS = {"X-Requested-With": "XMLHttpRequest"}
    SIGNUP_URL = "https://api.getimg.ai/dashboard/me"
    NEW_KEY_URL = "https://api.getimg.ai/dashboard/keys"
    MESSAGE_URL = "https://www.disposablemail.com/email/id/2"
    MESSAGES_URL = "https://www.disposablemail.com/index/refresh"
    NEW_EMAIL_URL = "https://www.disposablemail.com/index/index"
    
    def __init__(self, *, password: typing.Optional[str] = None) -> None:
        self.session = requests.Session()
        self.password = password if password else self.DEFAULT_PASSWORD


    def create_email(self) -> str:
        response = self.session.get(self.NEW_EMAIL_URL, headers=self.HEADERS)
        response.encoding = "utf-8-sig"
        return response.json().get("email")


    def register_email(self, email: str) -> None:
        payload = {
            "name": Faker("ja_JP").name(),
            "email": email,
            "password": self.password,
            "confirmPassword": self.password,
        }
        response = self.session.post(self.SIGNUP_URL, json=payload)
        
        if response.json().get("success", False):
            logger.success(f"Registered {email}")
        else:
            logger.error(f"Failed to register {email}")


    def get_messages(self) -> typing.List:
        response = self.session.get(self.MESSAGES_URL, headers=self.HEADERS)
        response.encoding = "utf-8-sig"
        return response.json()


    def wait_messsage(self, attempt: int = 30) -> None:
        curr_attempt = 0

        while curr_attempt < attempt:
            logger.debug(f"Attempt: {curr_attempt}")
            messages = self.get_messages()

            if len(messages) > 1:
                logger.success("Got a message")
                return

            logger.debug("Empty")
            curr_attempt += 1
            time.sleep(1)

    def activate_account(self) -> str:
        response = self.session.get(self.MESSAGE_URL)
        soup = BeautifulSoup(response.text, "lxml")
        activate_link = soup.select_one("td[valign=middle]>a").get("href")
        self.session.get(activate_link)
        logger.success("Account activated")

    def create_key(self) -> str:
        response = self.session.post(self.NEW_KEY_URL, json={"name": ""})
        return response.json().get("key")

    def write_api_key(self) -> None:
        email = self.create_email()
        logger.info(f"Email: {email}")
        self.register_email(email)
        self.wait_messsage()
        self.activate_account()
        key = self.create_key()
        
        self.session.close()
        
        filepath = paths.SETTINGS_DIR.joinpath("api.key")
        with open(filepath, "w") as file:
            file.write(key)
