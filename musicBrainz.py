import musicbrainzngs
from time import sleep
from os import remove, path

#prob do this idk
#musicbrainzngs.auth()
musicbrainzngs.set_useragent("Audio Downloader into MusicBrainz Tag for Local Audio (Need a better name lol)", "0.1", "Zach.Schultz.2.0.1@gmail.com")
    
def SearchDB(SongName: str):
    pass

def callDB(RecordingID: str) -> dict: # When we know the Song to get the Data from it
    while True: # Set this to some Time Out 
        try:
            Recording_Data = musicbrainzngs.get_recording_by_id(
                RecordingID,
                includes=[
                    'artists',
                    'releases',
                    'release-group-rels',
                    'media'
                ]
            )
            Release_Data = musicbrainzngs.get_release_by_id(
                Recording_Data['recording']['release-list'][0]['id'],
                includes=[
                    "release-groups",
                    "media"
                    ]
            )
            break
        except Exception as exc:
            print("Something went wrong with the request: %s" % exc)
            sleep(3)   
    
    

    recording = Recording_Data["recording"] 
    artist_credit = recording["artist-credit"]
    release_list = recording["release-list"][0] # we just take the first one
    medium_list = release_list["medium-list"][0]
    release = Release_Data['release']
    release_group = release['release-group']
    type = release_group['type']


    print(Release_Data)
    # Grabing Artist Data
    temp_artist = []
    temp_artist_ID = []

    for parts in artist_credit:
        if "artist" in parts:
            temp_artist.append(parts['artist']['name'])
            temp_artist_ID.append(parts['artist']['id'])
    
    song_info: dict = {
        'title': recording['title'],
        'artist': ';'.join(temp_artist),
        'album_artist': release_list['artist-credit'][0]['artist']['name'], # if type != "Single" else "",
        'album': release_list['title'], # if type != "Single" else "",
        'disc_number': medium_list['position'], 
        'total_discs': release['medium-count'],
        'track_number': medium_list['track-list'][0]['position'],
        'total_tracks': medium_list['track-count'],
        'release_date': release_list['date'],
        'year': release_list['date'].split("-")[0] if release_list['date'] != "" else "",
        'genre': "", #TODO
        'MB_album_artist_id': temp_artist_ID[0],
        'MB_album_id': release_list['id'],
        'MB_other_artist_id': temp_artist_ID[1] if len(temp_artist_ID) > 1 else "", 
        'MB_release_group_id': release_group['id'],
        'MB_release_id': release['id'],
        'MB_track_id': recording['id']
    } 
    
    print('title:',song_info['title'])
    print('artist:',song_info['artist'])
    print('album_artist:',song_info['album_artist'])
    print('album:',song_info['album'])
    print('disc_number:',song_info['disc_number'])
    print('total_discs:',song_info['total_discs'])
    print('track_number:',song_info['track_number'])
    print('total_tracks:',song_info['total_tracks'])
    print('release_data:',song_info['release_date'])
    print('year:',song_info['year'])
    print('MB_album_artist_id:',song_info['MB_album_artist_id'])
    print('MB_album_id:',song_info['MB_album_id'])
    print('MB_other_artist_id:',song_info['MB_other_artist_id'])
    print('MB_release_group_id:',song_info['MB_release_group_id'])
    print('MB_track_id:',song_info['MB_track_id'])
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
    
    
if __name__ == "__main__":
    print("API Test")
    ID = input("Enter ID: ")
    download_dir = 'downloads'
    cover_file = 'cover.jpg'
    song_info = callDB(ID)
    print(song_info)
    getcoverImage(song_info['MB_release_id'],download_dir,cover_file)
