#!/usr/bin/python3
import os
import time
from abc import abstractmethod
from pathlib import Path
from typing import Optional

from colorama import Fore
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumBot:
    # * for printing colours
    green = Fore.GREEN
    red = Fore.RED
    blue = Fore.BLUE
    magenta = Fore.MAGENTA
    reset = Fore.RESET

    def __init__(
        self,
        username: Optional[str],
        password: Optional[str],
        driver_path: str,
        path_to_save: str,
        data_dir: Optional[str] = None,
    ):
        self.username = username or None
        self.password = password or None

        self.driver_path = driver_path
        # this is come as command line input for completed code.
        self.images_folder_path = Path("path_to_save")
        self.success_folder_name = Path("success")
        self.error_folder_name = Path(r"error")
        self.data_dir = data_dir or f"{Path.cwd()}/data"

        if not os.path.exists(self.images_folder_path):
            os.mkdir(self.images_folder_path)

    def setupDriver(self, type: Optional[str]="chrome"):
        service = Service(executable_path=self.driver_path)

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument(
            f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        )
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--disable-browser-side-navigation")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-application-cache")
        chrome_options.add_argument("--allow-running-insecure-content")


        chrome_options.add_experimental_option(
            "prefs",
            {
                # ? for some reason had to hardcode the path
                "download.default_directory": r"<path_to_save>",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False,
                "profile.default_content_setting_values.automatic_downloads": 1,
            },
        )

        driver = webdriver.Chrome(chrome_options, service=service)
        # driver.maximize_window()
        return driver

    @abstractmethod
    def scroll(self, **kwargs):
        pass

    @abstractmethod
    def login(self, **kwargs):
        pass

    def cacheData(self, **kwargs):
        self.file = kwargs.get("path") or None
        self.data = kwargs.get("data") or None

        if not self.file:
            self.file = f"{self.data_dir}/urls.txt"

        if self.data:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            if os.path.exists(self.file):
                with open(self.file, "a+") as f:
                    f.write(f"{self.data}\n")
            # * just create the file
            else:
                with open(self.file, "w"):
                    pass

    def loadUrls(self, filepath: Optional[str] = None):
        if filepath:
            self.file = filepath
        if os.path.exists(self.file):
            # print(self.file)
            with open(self.file, "r") as f:
                data = f.readlines()
            return data
        return None

    @abstractmethod
    def imageDownalod(self, **kwargs):
        pass

    def isDownloadFinished(self):
        self.path = self.images_folder_path
        self.chrome_temp_file = sorted(Path(self.path).glob("*.crdownload"))
        self.downloaded_files = sorted(Path(self.path).glob("*.*"))

        # * something for future
        self.firefox_temp_file = sorted(Path(self.path).glob("*.part"))

        if (
            (len(self.firefox_temp_file) == 0)
            and (len(self.chrome_temp_file) == 0)
            and (len(self.downloaded_files) >= 1)
        ):
            return True
        else:
            return False
