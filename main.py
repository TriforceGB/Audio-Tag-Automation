# Libraries
from os import remove, rename, makedirs, path, getenv
from shutil import move


# File Imports
from Tagger import EditTag
from audio_downloader import download_audio
from musicBrainz import MusicBrainz_init,callDB,getcoverImage
from Cover_Edits import crop_cover
from ManualEdit import AddMissing, DictPrintout
from FileRenaming import cleanName, RenameSong

# API Key Imports
ACOUSTID_USER_API=getenv('ACOUSTID_USER_API')
ACOUSTID_APP_API=getenv('ACOUSTID_APP_API')
MUSICBRAINZ_USER=getenv('MUSICBRAINZ_USER')
MUSICBRAINZ_PASS=getenv('MUSICBRAINZ_PASS')

song_info: dict = {
    'title': "",
    'sort_title': "",
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
    'MB_album_artist_id': "",
    'MB_album_id': "",
    'MB_other_artist_id': "", 
    'MB_release_group_id': "",
    'MB_release_id': "",
    'MB_track_id': ""
} 

def Album_Folder(Music_Dir: str, album: str, filename: str) -> str:
    Song_Folder = f"{Music_Dir}\\{cleanName(album)}"
    makedirs(Song_Folder,exist_ok=True)
    return Song_Folder
    
def move_song(Song_Folder: str, Download_Dir: str, filename: str):
    move(path.join(Download_Dir,filename), path.join(Song_Folder,filename))
    



def main(Download_Dir: str, Music_Dir: str, askforID: bool, keepImages: bool, OnlyEnglishNames: bool) -> None: 
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
    MusicBrainz_init(MUSICBRAINZ_USER,MUSICBRAINZ_PASS)
    db_info = callDB(id,OnlyEnglishNames)
    song_info.update(db_info)
    print(song_info)
    getcoverImage(song_info['MB_release_id'],song_info['cover_path'])
    song_info['cropped_cover_path'] = crop_cover(song_info['cover_path'],Download_Dir)
    DictPrintout(song_info)
    AddMissing(song_info)
    EditTag(song_info)
    
    # Rename
    newName = RenameSong(song_info['audio_path'],Download_Dir,song_info['title'],song_info['album_artist'])
    
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
    OnlyEnglishNames = False
    Download_Dir = '.\\downloads'
    Music_Dir =  '.\\Done'#'S:\\mediafiles\\music'
    main(Download_Dir,Music_Dir,askforID,keepImages,OnlyEnglishNames)
