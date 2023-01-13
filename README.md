# wavclip-util

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
And the basic structure is as follows:
```yaml
origin: xxx.wav        # the big origin file, required
format: wav            # output format, always extensions such as mp3, defaultly "wav", optional

year: 2022             # the published year of all albums, globally, optional
album_artist: X        # set the default album artist of all albums, optional

albums:
  -
    title: XXX         # album name, required
    album_artist: Z    # album artist, optional
    year: 2023         # published year, optional
    parts:
      -
        name: A        # title of this song, required
        file: B        # specialized file name, excluding suffix, optional
        artist: Y      # specialized artist name, defaultly album artist
        from: '00:00'  # start time in the whole file, optional
                       # defaultly the last song's end time or 00:00 (if first song)
        to: '63:13'    # end time in the whole file, required
      -
        name: B
        file: C
        artist: Y & X
        to: '67:00'
  -
    title: YYY
    parts:
      -
        name: Foo
        to: '80:00'
#......
```
This example will produce 3 files: B.wav, C.wav and Foo.wav
(cafe.yml is a good example)

After that, run it to split file.
```
python3 wavclip-util.py cafe.yml
```
Default output directory is ".", add "-d <directory>" to change it.
```
python3 wavclip-util.py cafe.yml -d cafe
```

'cafe.yml' is an example including 2 albums, the origin audio file is of [here](https://www.youtube.com/watch?v=RY7FpB9BZH4).
