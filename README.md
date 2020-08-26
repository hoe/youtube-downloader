# youtube-downloader
helper for inserting music into itunes

# example
```
python main.py "https://www.youtube.com/watch?v=_r-nPqWGG6c" --title No Idea --artist Don Toliver --thumbnail --geckodriver "/Users/nick/Downloads/geckodriver"
```

# arguments
| argument      | description                                                  | example                                       |
|---------------|--------------------------------------------------------------|-----------------------------------------------|
| youtube       | The youtube link to the songs video, must surround in quotes | "https://www.youtube.com/watch?v=_r-nPqWGG6c" |
| --title       | The title of the music                                       | No Idea                                       |
| --artist      | The artist of the music                                      | Don Toliver                                   |
| --thumbnail   | If the music should include art                              |                                               |
| --geckodriver | Path to geckodriver, must surround in quotes                 | "/Users/example/Downloads/geckodriver"        |

# outcome
![Image](https://i.imgur.com/5KWJR0A.png)
