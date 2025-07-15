from os import path, rename, makedirs, remove
from shutil import move
from re import sub

def CleanName(name: str) -> str:
    # Clean up Name for Windows to be Happy
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    name = sub(invalid_chars, '', name)
    return name 

# Rename A File
def RenameSong(audio_path: str, Download_Dir: str, title: str, artist: str) -> str:
    newName = CleanName(f"{title} - {artist}.m4a")
    newPath = path.join(Download_Dir,newName)
    rename(audio_path,newPath)
    return newName,newPath

def AlbumFolder(Music_Dir: str, album: str) -> str:
    Song_Folder = f"{Music_Dir}\\{CleanName(album)}"
    makedirs(Song_Folder,exist_ok=True)
    return Song_Folder

def MoveSong(audio_path: str, Song_Folder: str, filename: str) -> None:
    newPath = path.join(Song_Folder,filename)
    if path.exists(newPath):
        remove(newPath)
    move(audio_path, newPath)

def RemoveCover(cover_path: str, cropped_cover_path: str) -> None:
    if path.exists(cover_path):
        remove(cover_path)
    if path.exists(cropped_cover_path):
        remove(cropped_cover_path)