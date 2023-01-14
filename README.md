# albumclip-util

## Overview

Utility script to split a huge music file into parts. Supports many music file formats such as wav, mp3, flac and so on.

## Installation

Following packages are required:
```
pydub
pyyaml
pytaglib
```
## Usage
To split the audio properly, a configuration file, which is written in YAML, is required.
And the syntax is as follows:(This is a part of [cafe.yml](cafe.yml))
```yaml
origin: cafe_de_touhou.mo3         # the big origin file, required
format: mp3                        # output format, always extensions such as mp3, defaultly "wav", optional

year: 2010                         # the published year of all albums, globally, optional
album_artist: DDBY                 # set the default album artist of all albums, optional

albums:
  -
    title: Cafe de Touhou          # album name, required
    album_artist: DDBY             # album artist, optional
    # year: 2010                   # published year, defaultly the global one, optional
    parts:
      -
        name: もし、空が晴れるなら # title of this song, required
        file: If the sky clears    # specialized file name, excluding suffix, optional
        artist: Bizen              # specialized artist name, defaultly album artist
        # from: '0:0'              # start time in the whole file, optional
                                   # defaultly the last song's end time or 00:00 (if first song)
        to: '4:14'                 # end time in the whole file, required
      -
        name: faraway country
        artist: 鯛の小骨
        to: '9:15'
  -
    title: Cafe de Touhou 2
    year: 2011
    parts:
      -
        name: かんぱんバカンス
        file: Cracker Holidays
        artist: 鯛の小骨
        from: '1:00:08'
        to: '1:05:05'
#......
```
After that, run it to split file.
```
python3 albumclip-util.py cafe.yml
```
Default output directory is ".", add "-d <directory>" to change it.
```
python3 albumclip-util.py cafe.yml -d cafe
```

The origin audio file of [cafe.yml](cafe.yml) is [here](https://www.youtube.com/watch?v=RY7FpB9BZH4).

## License

The whole project (albumclip-util.py and cafe.yml) is released under CC-BY-NC 4.0 license.
