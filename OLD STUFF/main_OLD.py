# Libraries
from os import remove, rename, makedirs, path, getenv
from shutil import move


# File Imports
from Tagger import EditTag
from audio_downloader import download_audio
from musicbrainz_fetch import MusicBrainz_init,callDB,getcoverImage
from cover_crop import CropCover
from ManualEdit import AddMissing, DictPrintout
from FileRenaming import cleanName, RenameSong
from acoust_id import getfingerprint

# Key Var to Edit the Download
keepImages = False
ManualTagging = False
ManualIntervention = True
Download_Dir = '.\\downloads'
Music_Dir = 'S:\\mediafiles\\music'

song_list = [
    'https://youtu.be/lBZeMeZrDEE?si=YrCDeXufXHmtjVMO'
    ]

# https://youtu.be/tUKNV2pPw0Q?si=9CaeAelFSFapBhX2
# https://youtu.be/EamxSv3xhoE?si=eSOFVwbLcLu327gL
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

   

    



def main(url: str,Download_Dir: str, Music_Dir: str, ManualTagging: bool, keepImages: bool, ManualIntervention: bool) -> None: 
    while True:
        try:
            dl_info = download_audio(url,Download_Dir,'m4a')
            break
        except Exception as e:
            print(e)
    song_info.update(dl_info)
    if ManualTagging == False:
        id = getfingerprint(song_info['audio_path'],ACOUSTID_APP_API,ManualIntervention)
        print(id)
        MusicBrainz_init(MUSICBRAINZ_USER,MUSICBRAINZ_PASS)
        db_info = callDB(id,ManualIntervention)
        song_info.update(db_info)
    # print(song_info)
    getcoverImage(song_info['MB_release_id'],song_info['cover_path'])
    song_info['cropped_cover_path'] = CropCover(song_info['cover_path'],Download_Dir)
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

    for url in song_list:
        main(url,Download_Dir,Music_Dir,ManualTagging,keepImages,ManualIntervention)
