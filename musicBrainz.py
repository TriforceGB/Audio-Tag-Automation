# Libraries
import musicbrainzngs
from time import sleep
# File Imports
from GenreChecker import CheckGenre
from FileRenaming import cleanName

# There prob a better way to init this but idc
def MusicBrainz_init(MUSICBRAINZ_USER:str, MUSICBRAINZ_PASS:str):
    musicbrainzngs.set_useragent("Audio Downloader into MusicBrainz Tag for Local Audio (Need a better name lol)", "0.2", "Zach.Schultz.2.0.1@gmail.com")
    musicbrainzngs.auth(MUSICBRAINZ_USER, MUSICBRAINZ_PASS)
    musicbrainzngs.set_format(fmt='json')

def callDB(RecordingID: str, UseEnglishNames: bool) -> dict: 
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
    
   

    # Already have 
    # recording
    # release
    # Spliting the Info into Useable Vars
    release_group = release['release-group']
    artist_credit = recording["artist-credit"]
    recording_media = recording['releases'][0]['media'][0] # Taking the first one becuase there should only be the info of the disc of the track we are reading from
    release_media = release["media"] 
    # type = release-group['primary-type'] not needed I think but show between an Album and a Single
            

    # Init all the Var
    title: str = ""
    sort_title: str = ""
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
    MB_album_artist_id: list = []
    MB_album_id: str = ""
    MB_other_artist_id: list = []
    MB_release_group_id: str = ""
    MB_release_id: str = ""
    MB_track_id: str = ""
    # Extra stuff needed for Getting MetaData
    tags: dict = []
    artist_id: dict = []
    
    # turn this into a def at some Point but Not Now
    
    # Setting Title
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
            title = input(f"No English Title Found for '{recording['title']}', Enter Title or Leave Blank for Original: ")
            sort_title = cleanName(title).lower()
    # If no Alias Exist
    elif UseEnglishNames == True:
        title = input(f"No alias found, Enter Title or leave blank for '{recording['title']}': ")
        sort_title = cleanName(title).lower()
            
    # A Catch All for if no Name is Inputed
    if title == "":
        title = recording['title']
        sort_title = cleanName(title).lower()
    
    # Grabing Artists 
    for artist_data in artist_credit:
        # Looking for English Name of Artist
        artist_name: str = ""
        if len(artist_data['artist']['aliases']) > 0:
            for aliases in artist_data['artist']['aliases']:
                if aliases['locale'] == "en" or aliases['locale'] == "[Worldwide]":
                    artist_name = aliases['name'] 
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
    # only take the 1 becuase Jellyfin doesn't support more then one
    # Looking for English Name of Artist
    album_artist_name: str = ""
    if len(release['artist-credit'][0]['artist']['aliases']) > 0:
        for aliases in release['artist-credit'][0]['artist']['aliases']:
            if aliases['locale'] == "en" or aliases['locale'] == "[Worldwide]":
                album_artist_name = aliases['name'] 
                break
        # What to do if no English Named found
        if album_artist_name == "" and UseEnglishNames == True:
            album_artist_name = input(f"No English Name Found for '{release['artist-credit'][0]['artist']['name']}', Enter Name or Leave Blank for Original: ")
    # If no Alias Exist
    elif UseEnglishNames == True:
        album_artist_name = input(f"No alias found, Enter album artist name or leave blank for {release['artist-credit'][0]['artist']['name']}: ")
        
    # A Catch All for if no Name is Inputed
    if album_artist_name == '':
        album_artist_name = release['artist-credit'][0]['artist']['name']
    # adding info to lists
    album_artist = album_artist_name
    MB_album_artist_id = release['artist-credit'][0]['artist']['id']
    
    
    # Grabing Album
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
            album = input(f"No English Name Found for Album '{release['title']}, Enter Name: ")
    else:
        album = input(f"No English Name Found for Album '{release['title']}, Enter Name: ")
            
            
            
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
    MB_release_id = release['id'] 
    MB_track_id = recording['id']
    
    # add all the meta data into a Dict
    song_info: dict = {
        'title': title, 
        'sort_title': sort_title,
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
        'MB_release_id': MB_release_id,
        'MB_track_id': MB_track_id 
        
    } 
    return song_info

def getcoverImage(release_id: dict, cover_path: str):
    try:
        image_data = musicbrainzngs.get_image_front(release_id)
        with open(cover_path, 'wb') as f:
            f.write(image_data)
    except Exception as exc:
        print("Something went wrong with the request: %s" % exc)
        
def submitTag(type: str, id: str, tag: str):
    pass #idk how this works
    
if __name__ == "__main__":
    print("API Test")
    from os import getenv
    MusicBrainz_init(getenv('MUSICBRAINZ_USER'),getenv('MUSICBRAINZ_PASS'))
    ID = input("Enter ID: ")
    download_dir = 'downloads'
    cover_file = '.\\downloads\\cover.jpg'
    NonAllowEnglishNames = True
    song_info = callDB(ID,True)
    print(song_info)
    getcoverImage(song_info['MB_release_id'],cover_file)
