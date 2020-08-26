import eyed3 as metadata
import youtube_dl
import argparse

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
    
    music = metadata.load(f"{name}.mp3")

    if arguments.title:
        music.tag.title = arguments.title

    if arguments.artist:
        music.tag.artist = arguments.artist

    if arguments.thumbnail and arguments.geckodriver:
        from scraper import Scraper

        scraper = Scraper(arguments.geckodriver, music)
        scraper.begin(name=name)

    music.tag.save()

if __name__ == "__main__":
    main()