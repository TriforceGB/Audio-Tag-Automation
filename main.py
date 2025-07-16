# Libraries
from shutil import move
from os import getenv
from yt_dlp import YoutubeDL
import json
# File Imports
from song import song
from youtube_downloads import PlaylistToURL
from musicbrainz_fetch import MusicBrainz_init

# API Key Imports
ACOUSTID_USER_API=getenv('ACOUSTID_USER_API')
ACOUSTID_APP_API=getenv('ACOUSTID_APP_API')
MUSICBRAINZ_USER=getenv('MUSICBRAINZ_USER')
MUSICBRAINZ_PASS=getenv('MUSICBRAINZ_PASS')

# Remove For Json Useage
# ManualTagging = False #If we Skip MusicBrainz and AcoustID and Just Manually Tag
# ManualIntervention = False # Attempts To make All decisions for you (Don't use if your dealing with Covers, Non Enlgish Artist or anything where you might need to Manually Change Something)
# MatchingAlbum = False # Make Sure All the Songs Have the Same Album as the First Song
# SubmitToDB = False # If The Code Submit Tags and Fingerprints Back to DB 
# DownloadDir = 'D:\\Code\\Mp3-Automation\\downloads'
# MusicDir = 'D:\\Code\\Mp3-Automation\\Done' #'S:\\mediafiles\\music'

def main():
    # Fetching the URL from File
    # Could be Removed With an GUI
    with open('download.json', 'r', encoding='utf-8') as file:
        download_json: dict = json.load(file)
    DownloadDir = download_json['DownloadDir']
    MusicDir = download_json['MusicDir']
    # Creating a List of Songs Objects
    for Groups in download_json['Groups']:
        ManualTagging = Groups['ManualTagging'] #If we Skip MusicBrainz and AcoustID and Just Manually Tag
        ManualIntervention = Groups['ManualIntervention'] # Attempts To make All decisions for you (Don't use if your dealing with Covers, Non Enlgish Artist or anything where you might need to Manually Change Something)
        MatchingAlbum = Groups['MatchingAlbum'] # Make Sure All the Songs Have the Same Album as the First Song
        SubmitToDB = Groups['SubmitToDB'] # If The Code Submit Tags and Fingerprints Back to DB 
        FirstSong_Song_Info: dict = None
        if 'Starting_Info' in Groups:
            FirstSong_Song_Info = Groups['Starting_Info']

        song_list: list = []
        for url in Groups['URLs']:
            if url.find("playlist") != -1: # If its a playlist is set to download just take the URL of the playlist
                playlist_urls = PlaylistToURL(url)  
                for playlist_url in playlist_urls:
                    song_list.append(song(playlist_url)) 
            else:                
                song_list.append(song(url))
        

        # Init MusicBrainz If we Using it.
        
        if ManualTagging == False:
            MusicBrainz_init(MUSICBRAINZ_USER,MUSICBRAINZ_PASS)
        # # Going Through Each Song in the List
        for music in song_list:
            music.youtube_fetch()
            music.youtube_download(DownloadDir)
                    
            # Goes to the 2 DB if we Enable Tagging Via DB
            if ManualTagging == False:
                music.acoustid_fingerprint(ACOUSTID_APP_API,ManualIntervention)
                if music.song_info['MB_track_id'] == "":
                    ManualTagging = True # Enable its for this Song if we are Manually Tagging
                else:
                    music.musicbrainz_search(ManualIntervention)
                    if FirstSong_Song_Info != None:
                        print("CONNECTISADFKLJASDJ:LKASDJKLASJL:D")
                        music.musicbrainz_album_correction(FirstSong_Song_Info)
                        
            AddedManualTag = music.manual_edit(ManualTagging) 
            music.cover(DownloadDir,ManualTagging,ManualIntervention)
            
            
           
            
            if SubmitToDB == True and ManualTagging == False:
                # music.print_info()
                # if input("Enter Y to Submit Info to MusicBrainz and AcoustID: " ).lower() == "y":
                    #Sending Changes to MusicBrainz Only if we added something manually
                if AddedManualTag == True:
                    music.musicbrainz_submit()
                # Adding my Info to the AcoustID DB
                music.acoustid_submit_fingerprint(ACOUSTID_APP_API,ACOUSTID_USER_API)
                if music.song_info['AcoustID'] == "":
                    music.acoustid_fingerprint(ACOUSTID_APP_API,ManualIntervention)
            ManualTagging = Groups['ManualTagging'] # Resetting the ManualTagging 
            music.add_tags()
            music.rename_song(DownloadDir)
            music.create_album_folder(MusicDir)
            music.move_song()
            music.remove_cover()
            if MatchingAlbum == True and FirstSong_Song_Info == None:
                FirstSong_Song_Info = music.song_info
        
            

if __name__ == "__main__":
    main()