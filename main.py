# Libraries
from shutil import move
from os import getenv
from yt_dlp import YoutubeDL
# File Imports
from song import song
from youtube_downloads import PlaylistToURL
from musicbrainz_fetch import MusicBrainz_init

# API Key Imports
ACOUSTID_USER_API=getenv('ACOUSTID_USER_API')
ACOUSTID_APP_API=getenv('ACOUSTID_APP_API')
MUSICBRAINZ_USER=getenv('MUSICBRAINZ_USER')
MUSICBRAINZ_PASS=getenv('MUSICBRAINZ_PASS')


ManualTagging = False # If we Skip MusicBrainz and 
ManualIntervention = True # If There is an decision That need User input do you ask or just pick the top Opition
MatchingAlbum = True # If the Album should all be the same
DownloadDir = 'D:\\Code\\Mp3-Automation\\downloads'
MusicDir = 'D:\\Code\\Mp3-Automation\\Done' #'S:\\mediafiles\\music'

def main():
    # Fetching the URL from File
    # Could be Removed With an GUI
    with open('download_list.txt') as file:
        url_list: list = [line.strip() for line in file]
        
    # Creating a List of Songs Objects
    song_list: list = []
    for url in url_list:
        if url.find("playlist") != -1: # If its a playlist is set to download just take the URL of the playlist
            playlist_urls = PlaylistToURL(url)  
            for playlist_url in playlist_urls:
                song_list.append(song(playlist_url)) 
        else:                
            song_list.append(song(url))
    

    # Init MusicBrainz If we Using it
    if ManualTagging == False:
        MusicBrainz_init(MUSICBRAINZ_USER,MUSICBRAINZ_PASS)
    # # Going Through Each Song in the List
    for music in song_list:
        music.youtube_fetch()
        music.youtube_download(DownloadDir)
                
        # Goes to the 2 DB if we Enable Tagging Via DB
        if ManualTagging == False:
            
            music.acoustid_fingerprint(ACOUSTID_APP_API,ManualIntervention)
            music.musicbrainz_search(ManualIntervention)
        
        music.crop_cover(DownloadDir)
        if music.manual_edit(ManualTagging):
            pass
            # Sending Changes to MusicBrainz Only if we added something manually
        #     music.musicbrainz_submit()
        # # Adding my Info to the AcoustID DB
        # music.acoustid_submit_fingerprint()
        music.add_tags()
        music.rename_song(DownloadDir)
        music.create_album_folder(MusicDir)
        music.move_song()
        music.remove_cover()
        
            

if __name__ == "__main__":
    main()