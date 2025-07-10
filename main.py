# Libraries
from os import remove, rename, makedirs, path
from shutil import move
from re import sub

# File Imports
from Tagger import EditTag
from audio_downloader import download_audio
from musicBrainz import callDB,getcoverImage
from Cover_Edits import crop_cover
from ManualEdit import AddMissing, DictPrintout


song_info: dict = {
    'title': "",
    'artist': [],
    'album_artist': "",
    'album': "",
    'disc_number': "",
    'total_discs': "",
    'track_number':"",
    'total_tracks': "",
    'release_date': "",
    'year': "",
    'genre': [], 
    'audio_path': "",
    'cover_path': "",
    'cropped_cover_path': "",
    'acoustid': "",
    'MB_album_artist_id': "",
    'MB_album_id': "",
    'MB_other_artist_id': "", 
    'MB_release_group_id': "",
    'MB_release_id': "",
    'MB_track_id': ""
} 

def cleanName(name: str) -> str:
    # Clean up Name for Windows to be Happy
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
    name = sub(invalid_chars, '', name)
    return name 

def rename_song(audio_path: str, Download_Dir: str, title: str, artist: str) -> str:
    # Rename
    newName = cleanName(f"{title}-{artist}.m4a")
    rename(audio_path,path.join(Download_Dir,newName))
    return newName

def Album_Folder(Music_Dir: str, album: str, filename: str) -> str:
    Song_Folder = f"{Music_Dir}\\{cleanName(album)}"
    makedirs(Song_Folder,exist_ok=True)
    return Song_Folder
    
def move_song(Song_Folder: str, Download_Dir: str, filename: str):
    move(path.join(Download_Dir,filename), path.join(Song_Folder,filename))
    

def main(Download_Dir: str, Music_Dir: str, askforID: bool, keepImages: bool) -> None: 
    while True:
        try:
            url = input("Enter YouTube video URL: ")
            dl_info = download_audio(url,Download_Dir,'m4a')
            break
        except Exception as e:
            print(e)
    song_info.update(dl_info)
    if askforID:
        id = input("Enter ID: ")
    else:
        pass #Where we Search for the Song
    db_info = callDB(id)
    song_info.update(db_info)
    print(song_info)
    getcoverImage(song_info['MB_release_id'],song_info['cover_path'])
    song_info['cropped_cover_path'] = crop_cover(song_info['cover_path'],Download_Dir)
    DictPrintout(song_info)
    AddMissing(song_info)
    EditTag(song_info)
    
    # Rename
    newName = rename_song(song_info['audio_path'],Download_Dir,song_info['title'],song_info['album_artist'])
    
    # Create Folder
    AlbumFolder = Album_Folder(Music_Dir,song_info['album'],newName)
    

    # Move Song
    move_song(AlbumFolder,Download_Dir,newName)
    
    # Delete Images
    if keepImages:
        pass
    else:
        remove(song_info['cover_path'])
        remove(song_info['cropped_cover_path'])
    

if __name__ == "__main__":
    keepImages = False
    askforID = True
    Download_Dir = '.\\downloads'
    Music_Dir = '.\\Done'
    main(Download_Dir,Music_Dir,askforID,keepImages)
