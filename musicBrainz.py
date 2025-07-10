# Libraries
import musicbrainzngs
from time import sleep
from os import remove, path
# File Imports
from GenreChecker import CheckGenre

#TODO
#add auth so I can Submit Tags
#musicbrainzngs.auth()
# Setting User Agent to use API
# There prob a better way to init this but idc
musicbrainzngs.set_useragent("Audio Downloader into MusicBrainz Tag for Local Audio (Need a better name lol)", "0.2", "Zach.Schultz.2.0.1@gmail.com")


def callDB(RecordingID: str) -> dict: 
    # Take the Recording ID and find the rest of the MetaData
    while True: #TODO Set this to some Time Out 
        # Calling the API to get all the Info I need 
        try:
            Recording_Data = musicbrainzngs.get_recording_by_id(
                RecordingID,
                includes=[
                    'artists',
                    'releases',
                    'release-group-rels',
                    'media',
                    'tags'
                    
                ]
            )
            Release_Data = musicbrainzngs.get_release_by_id(
                Recording_Data['recording']['release-list'][0]['id'],
                includes=[
                    "release-groups",
                    "media"
                    ]
            )
            Release_Group_Data = musicbrainzngs.get_release_group_by_id(
                Release_Data['release']['release-group']['id'],
                includes=[
                    'tags'
                    ]
            )
            break
        except Exception as exc:
            print("Something went wrong with the request: %s" % exc)
            sleep(3)   
    
    # Spliting the Info into Useable Vars
    recording = Recording_Data["recording"] 
    artist_credit = recording["artist-credit"]
    release_list = recording["release-list"][0] # we just take the first one
    medium_list = release_list["medium-list"][0]
    release = Release_Data['release']
    release_group = release['release-group']
    type = release_group['type']
    
    

            
    # Grabing Artist Data
    artist: list
    artist_ID: list

    for parts in artist_credit:
        if "artist" in parts:
            artist.append(parts['artist']['name'])
            artist_ID.append(parts['artist']['id'])
            
    # Grabing Genres
    tags: dict
    Genres: list
    
    if 'tag-list' in recording: # Uses the Tags on the Recording First
        tags = recording['tag-list']
    elif 'tag-list' in Release_Group_Data['release-group']: # If Recording Tags don't Exist Use the ones on the Release Group
        tags = Release_Group_Data['release-group']['tag-list']
    
    for tag in tags: # Check all the Tags for the Genres
        if CheckGenre(tag['name']):
            Genres.append(tag['name'])
    
    # add all the meta data into a Dict
    song_info: dict = {
        'title': recording['title'],
        'artist': artist,
        'album_artist': release_list['artist-credit'][0]['artist']['name'], # if type != "Single" else "",
        'album': release_list['title'], # if type != "Single" else "",
        'disc_number': medium_list['position'], 
        'total_discs': release['medium-count'],
        'track_number': medium_list['track-list'][0]['position'],
        'total_tracks': medium_list['track-count'],
        'release_date': release_list['date'],
        'year': release_list['date'].split("-")[0] if release_list['date'] != "" else "",
        'genre': Genres,
        'MB_album_artist_id': artist_ID[0],
        'MB_album_id': release_list['id'],
        'MB_other_artist_id': artist_ID[1] if len(artist_ID) > 1 else "", 
        'MB_release_group_id': release_group['id'],
        'MB_release_id': release['id'],
        'MB_track_id': recording['id']
    } 
    return song_info

def getcoverImage(release_id: dict, cover_path: str):
    while True: # need some edge case for t to time out and if a cover is not found
        try:
            image_data = musicbrainzngs.get_image_front(release_id)
            break
        except Exception as exc:
            print("Something went wrong with the request: %s" % exc)
            sleep(3)   
    
    print(cover_path)
    with open(cover_path, 'wb') as f:
        f.write(image_data)
        
def submitTag(type: str, id: str, tag: str):
    pass #idk how this works
    
    
if __name__ == "__main__":
    print("API Test")
    ID = input("Enter ID: ")
    download_dir = 'downloads'
    cover_file = 'cover.jpg'
    song_info = callDB(ID)
    print(song_info)
    getcoverImage(song_info['MB_release_id'],download_dir,cover_file)
