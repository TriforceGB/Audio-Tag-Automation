# Libraries
import musicbrainzngs
from time import sleep
# File Imports
from genre_checker import CheckGenre
from file_management import CleanName

# There prob a better way to init this but idc
def MusicBrainz_init(MUSICBRAINZ_USER:str, MUSICBRAINZ_PASS:str):
    musicbrainzngs.set_useragent("RTX Auto Audio Tagger 3090 Inator", "0.5", "Zach.Schultz.2.0.1@gmail.com")
    musicbrainzngs.auth(MUSICBRAINZ_USER, MUSICBRAINZ_PASS)
    musicbrainzngs.set_format(fmt='json')

def MusicBrainzFetch(RecordingID: str, UseEnglishNames: bool) -> dict: 
    # Take the Recording ID and find the rest of the MetaData
    while True: #TODO Set this to some Time Out 
        # Calling the API to get all the Info I need 
        try:
            recording = musicbrainzngs.get_recording_by_id(
                RecordingID,
                includes=[
                    'aliases',
                    'artists',
                    'media',
                    'releases',
                    'tags',
                ]
            )
            # Grab the English Release
            release_id:str = recording['releases'][0]['id'] # backup the first one
            for release_lang in recording['releases']:
                if release_lang['text-representation']['language'] == 'eng' or release_lang['text-representation']['language'] == 'mul':
                    release_id = release_lang['id'] # Get the Release ID for the English Label
                    break
            release = musicbrainzngs.get_release_by_id(
                release_id,
                includes=[
                    "release-groups",
                    "artists",
                    "media",
                    "aliases",
                    'tags',
                    ]
            )
            break
        except Exception as exc:
            print("Something went wrong with the request: %s" % exc)
            sleep(3)   
    
   

    # Spliting the Info into Useable Vars
    release_group = release['release-group']
    artist_credit = recording["artist-credit"]
    recording_media = recording['releases'][0]['media'][0] # Taking the first one becuase there should only be the info of the disc of the track we are reading from
    release_media = release["media"] 
    # type = release-group['primary-type'] not needed I think but show between an Album and a Single
            

    # Init all the Var
    title: str = ""
    sort_title: str = ""
    original_title: str = ""
    artist: list = []
    album_artist: list = []
    album:str = ""
    disc_number: int = 0
    total_discs: int = 0
    track_number: int = 0
    total_tracks: int = 0
    release_date: str = ""
    year: str = ""
    genre: list = []
    MB_album_artist_id: str = ""
    MB_album_id: str = ""
    MB_other_artist_id: list = []
    MB_release_group_id: str = ""
    MB_track_id: str = ""
    # Extra stuff needed for Getting MetaData
    tags: dict = []
    artist_id: dict = []
    
    # turn this into a def at some Point but Not Now
    # Setting Title
    # Original Title Without Aliases
    original_title = recording['title']
    # Looking for the English One
    if len(recording['aliases']) > 0:
        for aliases in recording['aliases']:
            print(aliases['locale'])
            if aliases['locale'] == "en" or aliases['locale'] == "[Worldwide]":
                title = aliases['name']
                sort_title = aliases['sort-name']
                break
        # What to Do if No English Title found
        if title == "" and UseEnglishNames == True:
            title = input(f"No English Title Found for '{original_title}', Enter Title or Leave Blank for Original: ")
            sort_title = CleanName(title).lower()
    # If no Alias Exist
    elif UseEnglishNames == True:
        title = input(f"No alias found, Enter Title or leave blank for '{original_title}': ")
        sort_title = CleanName(title).lower()
            
    # A Catch All for if no Name is Inputed
    if title == "":
        title = original_title
        sort_title = CleanName(title).lower()
    
    # Grabing Artists
    for artist_data in artist_credit:
        # Looking for English Name of Artist
        artist_name: str = ""
        if len(artist_data['artist']['aliases']) > 0:
            # First looks for a Primary English Name then Just an English Name
            for Primary_loop in range(2):
                for aliases in artist_data['artist']['aliases']:
                    if aliases['primary'] == True or Primary_loop == 1: #Only Enter Name if its a Primary Name or its the second loop
                        if aliases['locale'] == "en" or aliases['locale'] == "[Worldwide]":
                            artist_name = aliases['name'] 
                            break
                if artist_name != "":
                    break
            # What to do if no English Named found
            if artist_name == "" and UseEnglishNames == True:
                artist_name = input(f"No English Name Found for '{artist_data['name']}', Enter Name or Leave Blank for Original: ")
        # If no Alias Exist
        elif UseEnglishNames == True:
            artist_name = input(f"No alias found, Enter artist name or leave blank for {artist_data['name']}: ")
            
        # A Catch All for if no Name is Inputed
        if artist_name == '':
            artist_name = artist_data['name']
        # adding info to lists
        artist.append(artist_name)
        # Finding if the ID is for a other artist or album artist
        for album_artists_data in release_group['artist-credit']:
            if artist_data['artist']['id'] !=  album_artists_data['artist']['id']:
                artist_id.append(artist_data['artist']['id'])


    # Grabing Album Artist
    for artist_data in release['artist-credit']:
        # Looking for English Name of Artist
        artist_name: str = ""
        if len(artist_data['artist']['aliases']) > 0:
            # First looks for a Primary English Name then Just an English Name
            for Primary_loop in range(2):
                for aliases in artist_data['artist']['aliases']:
                    if aliases['primary'] == True or Primary_loop == 1: #Only Enter Name if its a Primary Name or its the second loop
                        if aliases['locale'] == "en" or aliases['locale'] == "[Worldwide]":
                            artist_name = aliases['name'] 
                            break
                if artist_name != "":
                    break
            # What to do if no English Named found
            if artist_name == "" and UseEnglishNames == True:
                artist_name = input(f"No English Name Found for '{artist_data['name']}', Enter Name or Leave Blank for Original: ")
        # If no Alias Exist
        elif UseEnglishNames == True:
            artist_name = input(f"No alias found, Enter Album Artist name or leave blank for {artist_data['name']}: ")
            
        # A Catch All for if no Name is Inputed
        if artist_name == '':
            artist_name = artist_data['name']
        # adding info to lists
        album_artist.append(artist_name)
        if MB_album_artist_id == "":
            MB_album_artist_id = artist_data['artist']['id']
        
    # Grabing Album
    # If using the First Sone Album
    # This may Need to be change depening if all Album Artist Match the Album Lanaguage
    # Looking for English Title 
    if release['text-representation']['language'] == "eng" or UseEnglishNames == False:
        album = release['title']
    elif len(release_group['aliases']) > 0:
        for aliases in release_group['aliases']:
            if aliases['locale'] == "en" or aliases['locale'] == "[Worldwide]":
                album = aliases['name']
                break
        if album == "" and UseEnglishNames == True: 
            album = input(f"No English Name Found for Album, Enter Name or Leave Blank for: '{release['title']}: ")
    else:
        album = input(f"No English Name Found for Album, Enter Name or Leave Blank for: '{release['title']}: ")
    # A Catch All for if no Name is Inputed
    if album == '':
        album = release['title']
        
        
            
    # Grabing Genres
    if len(recording['tags']) > 0: # Uses the Tags on the Recording First
        tags = recording['tags']
    elif len(release['tags']) > 0: # If Recording Tags don't Exist Use the ones on the Release 
        tags = release['tags']
    elif len(release_group['tags']) > 0: # If Release Tags don't Exist Use the ones on the Release Group
        tags = release_group['tags']
    
    for tag in tags: # Check all the Tags for the Genres
        if CheckGenre(tag['name']):
            genre.append(tag['name'])

    # Adding all the Var to the Dict
    disc_number = recording_media['position']
    total_discs = len(release_media) 
    track_number = recording_media['tracks'][0]['position'] # Uses First becuase there should only be one track
    total_tracks = recording_media['track-count'] 
    release_date = recording['first-release-date']
    year = release_date.split("-")[0] if release_date != "" else "" # Take the Date and display nothing if date doesn't exist
    MB_album_id = release['id'] 
    MB_other_artist_id = artist_id[0] if len(artist_id) > 0 else "" # only take the first one becuase Jellyfin doesn't support more then one
    MB_release_group_id = release_group['id'] 
    MB_track_id = recording['id']
    
    # add all the meta data into a Dict
    song_info: dict = {
        'title': title, 
        'sort_title': sort_title,
        'original_title': original_title,
        'artist': artist,
        'album_artist': album_artist,
        'album': album, 
        'disc_number': disc_number, 
        'total_discs': total_discs,
        'track_number': track_number,
        'total_tracks': total_tracks,
        'release_date': release_date,
        'year': year,
        'genre': genre,
        'MB_album_artist_id': MB_album_artist_id,
        'MB_album_id': MB_album_id ,
        'MB_other_artist_id': MB_other_artist_id, 
        'MB_release_group_id': MB_release_group_id,
        'MB_track_id': MB_track_id 
    } 
    return song_info
# Editing the Song infomation if this is Apart of an Album and 
def MusicBrainzAlbumCorrection(original_info:dict, first_song_info:dict):
    update_info: dict = {
        'album_artist': original_info['album_artist'],
        'album': original_info['album'],
        'disc_number': original_info['disc_number'],
        'total_discs': original_info['total_discs'],
        'track_number': original_info['track_number'],
        'total_tracks': original_info['total_tracks'],
        'MB_album_artist_id': original_info['MB_album_artist_id'],
        'MB_album_id': original_info['MB_album_id'],
        'MB_release_group_id': original_info['MB_release_group_id'],
        }
    if original_info['MB_album_id'] != first_song_info['MB_album_id']:
        # Get The Track info for the Album
        try:
            album_info = musicbrainzngs.get_release_by_id(first_song_info['MB_album_id'],['recordings','artist-credits','release-groups'])
        except Exception as exc:
            print("Something went wrong with the request: %s" % exc)
        
        # Check if the Song is in the Album
        ChangesMade = False
        for disc in album_info['media']:
            for song in disc['tracks']:
                song['recording']['id'] == original_info['MB_track_id']
                if song['recording']['id'] == original_info['MB_track_id']:
                    new_song_info: dict = {
                        'album_artist': first_song_info['album_artist'],
                        'album': album_info['title'],
                        'disc_number': disc['position'],
                        'total_discs': len(album_info['media']),
                        'track_number': song['position'],
                        'total_tracks': len(disc['tracks']),
                        'MB_album_artist_id': album_info['artist-credit'][0]['artist']['id'], #Takes the First one becuase Jellyfin doesn't support more then one
                        'MB_album_id': first_song_info['MB_album_id'],
                        'MB_release_group_id': album_info['release-group']['id'],
                        }
                    update_info.update(new_song_info)
                    print("Changes Made")
                    ChangesMade = True
                    break
            if ChangesMade == True:
                break
        if ChangesMade == False:
            print("Song not found in Album, Skipping")
    return update_info
def getCoverImage(release_id: dict, cover_path: str):
    try:
        image_data = musicbrainzngs.get_image_front(release_id)
        with open(cover_path, 'wb') as f:
            f.write(image_data)
    except Exception as exc:
        print("Something went wrong with the request: %s" % exc)
        
def SubmitTag(id: str, tags: list):
    musicbrainzngs.submit_tags(recording_tags={id:tags})
    
if __name__ == "__main__":
    print("API Test")
    from os import getenv
    MusicBrainz_init(getenv('MUSICBRAINZ_USER'),getenv('MUSICBRAINZ_PASS'))
    # original_song = {'title': 'New Battle!!!', 'sort_title': 'new battle!!!', 'original_title': 'New Battle!!!', 'artist': ['Kenji Hiramatsu'], 'album_artist': 'Yasunori Mitsuda', 'album': 'Xenoblade Chronicles Original Soundtrack Trinity Box', 'disc_number': 20, 'total_discs': 20, 'track_number': 2, 'total_tracks': 14, 'release_date': '2023-07-29', 'year': '2023', 'genre': [], 'MB_album_artist_id': '118bf512-9ce9-42a5-95e0-10359bb3e3ea', 'MB_album_id': '96046f65-3c92-4414-9101-b81fce5797de', 'MB_other_artist_id': '252ea5d7-bc86-4278-9310-fe75910c6eb9', 'MB_release_group_id': '360e5c9f-0938-47c6-ba33-dc9579d78a69', 'MB_track_id': 'c5f9d90b-62e6-4760-a262-e424d0e1499e'}
    # song_need_to_edit = {'title': 'Drifting Soul', 'sort_title': 'drifting soul', 'original_title': 'Drifting Soul', 'artist': ['ACE'], 'album_artist': 'Yasunori Mitsuda', 'album': 'Xenoblade Chronicles 2 Original Soundtrack', 'disc_number': 2, 'total_discs': 5, 'track_number': 19, 'total_tracks': 19, 'release_date': '2018-05-23', 'year': '2018', 'genre': [], 'MB_album_artist_id': '118bf512-9ce9-42a5-95e0-10359bb3e3ea', 'MB_album_id': 'f18cd4a0-a774-438a-ad92-91405d04690f', 'MB_other_artist_id': '16563fb9-c2b5-4ab7-b5b1-7b6592f862a1', 'MB_release_group_id': 'ac8415c6-cf92-4016-9d08-fbc05e566e6b', 'MB_track_id': '13fe8646-d71f-41e5-a368-98d62876a2ff'}
    # print(MusicBrainzAlbumCorrection(song_need_to_edit,original_song))
    ID = input("Enter ID: ")
    download_dir = 'downloads'
    cover_file = '.\\downloads\\cover.jpg'
    NonAllowEnglishNames = True
    song_info = MusicBrainzFetch(ID,True)
    print(song_info)
    getCoverImage(song_info['MB_album_id'],cover_file)
