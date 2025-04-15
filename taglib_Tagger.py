# Currntly Unused
from taglib import File as Tag

def ChangeTag(raw_dir,files,title,artist,album,track_num,cover):
    try:
        for index in range(len(files)):
            with Tag(raw_dir+"\\"+files[index]) as song:
                song.tags["TITLE"] = title[index]
                song.tags["ARTIST"] = artist[index]
                song.tags["ALBUM"] = album[index]
                song.tags["TRACKNUMBER"] = track_num[index]
                song.save()
            print(index)
    except Exception as e:
        print(e)
