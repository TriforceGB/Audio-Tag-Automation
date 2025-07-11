from re import sub
from os import rename, path

def cleanName(name: str) -> str:
    # Clean up Name for Windows to be Happy
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    name = sub(invalid_chars, '', name)
    return name 

def RenameSong(audio_path: str, Download_Dir: str, title: str, artist: str) -> str:
    # Rename
    newName = cleanName(f"{title} - {artist}.m4a")
    rename(audio_path,path.join(Download_Dir,newName))
    return newName