import json
from pathlib import Path

import requests
from colorama import Fore

from impulse.SMS import random_data

SERVICES_PATH = "impulse/SMS/services.json"
PROXY_PATH = "impulse/SMS/proxy.json"


def getServices(filename: str | None = SERVICES_PATH) -> str:
    """Read services file."""
    with Path(filename).open(encoding="utf-8", errors="ignore") as services:
        return json.load(services)["services"]


def getProxys(filename: str | None = PROXY_PATH) -> str:
    """Read proxy list."""
    with Path(filename).open() as proxys:
        return json.load(proxys)["proxy"]


def getDomain(url: str):
    """Get domain by big url."""
    return url.split("/")[2]


def transformPhone(phone: str, i: int):
    """Make for other services (for Pizzahut).

    Example: '+7 (915) 350 99 08'
    """
    if i == 5:  # noqa: PLR2004
        return (
            "+"
            + phone[0]
            + " ("
            + phone[1:4]
            + ") "
            + phone[4:7]
            + " "
            + phone[7:9]
            + " "
            + phone[9:11]
        )
    return None


# Headers for request
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept-Encoding": "gzip, deflate, br",
    "User-agent": random_data.random_useragent(),
}


# Service class
# parseData, SendSMS
class Service:
    def __init__(self, service):
        self.service = service
        self.proxy = getProxys()
        self.timeout = 10

    # Parse string
    def parseData(self, phone):
        payload = None
        # Check for 'data'
        if "data" in self.service:
            dataType = "data"
            payload = self.service["data"]
        # Check for 'json'
        elif "json" in self.service:
            dataType = "data"
            payload = self.service["json"]
        # Check for 'url'
        else:
            payload = json.dumps({"url": self.service["url"]})
            dataType = "url"
        # Replace %phone%, etc.. to data
        for old, new in {
            "'": '"',
            "%phone%": phone,
            "%phone5%": transformPhone(phone, 5),
            "%name%": random_data.random_name(),
            "%email%": random_data.random_email(),
            "%password%": random_data.random_password(),
            "%token%": random_data.random_token(),
        }.items():
            if old in payload:
                payload = payload.replace(old, new)
        return json.loads(payload), dataType

    # Send message
    def sendMessage(self, phone):
        url = self.service["url"]
        payload, dataType = self.parseData(phone)

        # Add custom headers
        if "headers" in self.service:
            customHeaders = self.service["headers"]
            for key, value in json.loads(customHeaders.replace("'", '"')).items():
                headers[key] = value

        # Create suffixes
        okay = f"{Fore.YELLOW}Service ({getDomain(url)}) >> Message sent!{Fore.RESET}"
        error = f"{Fore.MAGENTA}Service ({getDomain(url)}) >> Failed to sent message!{Fore.RESET}"

        session = requests.Session()
        request = requests.Request("POST", url)
        request.headers = headers

        if dataType == "json":
            request.json = payload
        elif dataType == "data":
            request.data = payload
        elif dataType == "url":
            request.url = payload["url"]

        try:
            request = request.prepare()
            r = session.send(request, timeout=self.timeout, proxies=self.proxy)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            print(f"{Fore.RED}[CONNECTION TIMED OUT] {error}")
        except requests.exceptions.ConnectionError:
            print(f"{Fore.RED}[CONNECTION ERROR] {error}")
        except Exception as err:
            print(err)
        else:
            # Check status
            if r.status_code == 200:
                print(f"{Fore.GREEN}[SUCCESS] {okay}")
            elif r.status_code == 429:
                print(f"{Fore.RED}[TOO MANY REQUESTS] {error}")
            else:
                print(f"{Fore.RED}[{r.status_code}] {error}")
