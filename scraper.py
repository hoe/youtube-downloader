from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

from PIL import Image
from io import BytesIO
import requests
import os

class Scraper:
    """ attempts to use google to get artwork for the music file """

    def __init__(self, geckodriver, metadata):
        self.options = Options()
        self.options.headless = True
        self.browser = webdriver.Firefox(executable_path=geckodriver, service_log_path=os.path.devnull, options=self.options)
        self.metadata = metadata

    def begin(self, name: str) -> None:
        self.browser.get(f"https://www.google.com/search?q={name} art imagesize:500x500&tbm=isch&sclient=imgs")
        self.browser.find_element_by_xpath("//div//div//div//div//div//div//div//div//div//div[1]//a[1]//div[1]//img[1]").click()
        
        image = self.browser.find_element_by_xpath("//body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img")
        response = requests.get(image.get_attribute("src"))

        image = Image.open(BytesIO(response.content))
        image.save(f"{name}.jpg")

        self.browser.quit()

        with open(f"{name}.jpg", "rb") as image:
            self.metadata.tag.images.set(3, image.read(), "image/jpeg")

        os.remove(f"{name}.jpg") 

        return None