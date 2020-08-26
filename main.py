import eyed3 as metadata
from io import BytesIO
from PIL import Image
import youtube_dl
import subprocess
import argparse
import requests
import os

def main():
    parser = argparse.ArgumentParser(description="Help with the process of putting a song in Apple Music.")
    parser.add_argument("youtube", default=None, help="The youtube link to the songs video, must surround in quotes")
    parser.add_argument("--title", nargs="+", default=None, help="The title of the music")
    parser.add_argument("--artist", nargs="+", default=None, help="The artist of the music")
    parser.add_argument("--thumbnail", action="store_true", help="If the music should include art")
    parser.add_argument("--geckodriver", default=None, help="Path to geckodriver, must surround in quotes")

    arguments = parser.parse_args()

    arguments.title = " ".join(arguments.title)
    arguments.artist = " ".join(arguments.artist)

    name = f"{arguments.artist} - {arguments.title}"

    options = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": f"{name}.%(ext)s"
    }

    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([arguments.youtube])
    
    song = metadata.load(f"{name}.mp3")

    if arguments.title:
        song.tag.title = arguments.title

    if arguments.artist:
        song.tag.artist = arguments.artist

    if arguments.thumbnail and arguments.geckodriver:
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.firefox.options import Options
        from selenium import webdriver

        options = Options()
        options.headless = True

        browser = webdriver.Firefox(executable_path=arguments.geckodriver, service_log_path=os.path.devnull, options=options)
        browser.get(f"https://www.google.com/search?q={name} art filesize:500x500&tbm=isch&sclient=imgs")
        browser.find_element_by_xpath("//div//div//div//div//div//div//div//div//div//div[1]//a[1]//div[1]//img[1]").click()
        
        image = browser.find_element_by_xpath("//body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img")

        response = requests.get(image.get_attribute("src"))
        image = Image.open(BytesIO(response.content))
        image.save(f"{name}.jpg")

        browser.quit()

        with open(f"{name}.jpg", "rb") as artwork:
            song.tag.images.set(3, artwork.read(), "image/jpeg")

        os.remove(f"{name}.jpg")

    song.tag.save()

if __name__ == "__main__":
    main()
