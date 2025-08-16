# Libraries
from mutagen.mp4 import MP4, MP4Cover, MP4FreeForm
from genre_checker import CheckGenre

# Uses Mutagen to Tag all the M4A
# Only Support M4A becuase idk i'm wried

def ManualAddTag(song_info: dict, ManualTagging: bool, AddGenre: bool) -> bool:
    ChangeMade: bool = False
    for key, value in song_info.items():
        if ((value == "" or value == []) and key != 'MB_other_artist_id' and key != 'AcoustID' and (key == "genre" and AddGenre == True)) or ManualTagging == True:
            if key == "artist" or key == "album_artist" or key == "genre":
                print("----------")
                print(f"info missing: {key}")
                newList = []
                while True:
                    newvalue = input("Enter Value or Space to end: ")
                    if newvalue == "":
                        break
                    else: 
                        if key == "genre" and not CheckGenre(newvalue):
                            continue
                        newList.append(newvalue)
                    if len(newList) > 0:
                        ChangeMade = True
                        song_info[key] = newList
            else:
                print("----------")
                print(f"info missing: {key}")
                value = input(f"Enter Value: ")
                if value != "":
                    ChangeMade == True
                    song_info[key] = value 
                
    return song_info, ChangeMade
def EditTag(song_info: dict, audio_path: str, cover_path: str) -> None:
    # Grabs the Crop Cover Image
    with open(cover_path, 'rb') as f:
        cover_data = f.read()
        cover = MP4Cover(cover_data,imageformat=MP4Cover.FORMAT_JPEG)
    # Tag List in wried names becuase of stuff Not sure
    # Just find the List on Mutagen Docs
    song = MP4(audio_path)
    song["\xa9nam"] = song_info['title']
    song["----:com.apple.iTunes:SORT_TITLE"] = MP4FreeForm(song_info['sort_title'].encode('utf-8'))
    song["\xa9ART"] = song_info['artist']
    song["aART"] = song_info['album_artist']
    song["\xa9alb"] = song_info['album']
    if song_info['disc_number'] != "" and song_info['total_discs'] != "":
        song["disk"] = [(int(song_info['disc_number']), int(song_info['total_discs']))] 
    if song_info ['track_number'] != "" and song_info['total_tracks'] != "":
        song["trkn"] = [(int(song_info['track_number']), int(song_info['total_tracks']))]
    song["\xa9day"] = song_info['release_date']
    song["\xa9gen"] = song_info['genre']
    song["covr"] = [cover]
    # Custom Tags for Musicbrain
    song["----:com.apple.iTunes:MUSICBRAINZ_ALBUMARTISTID"] = MP4FreeForm(song_info['MB_album_artist_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_ALBUMID"] = MP4FreeForm(song_info['MB_album_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_ARTISTID"] = MP4FreeForm(song_info['MB_other_artist_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_RELEASEGROUPID"] = MP4FreeForm(song_info['MB_release_group_id'].encode('utf-8'))    
    song["----:com.apple.iTunes:MUSICBRAINZ_RELEASETRACKID"] = MP4FreeForm(song_info['MB_track_id'].encode('utf-8'))
    song["----:com.apple.iTunes:ACOUSTID_ID"] = MP4FreeForm(song_info['AcoustID'].encode('utf-8'))
    # Maybe add the acoustid not sure
    song.save()
    
# For Testing Only
if __name__ == "__main__":
    song_info = {'title': 'Golden', 'file-name': 'Golden', 'artist': 'HUNTR/X;이재;AUDREY NUNA;REI AMI;KPop Demon Hunters Cast', 'album_artist': 'KPop Demon Hunters Cast', 'album': 'KPop Demon Hunters (Soundtrack from the Netflix Film)', 'disc_number': '1', 'total_discs': 1, 'track_number': '4', 'total_tracks': 12, 'release_date': '2025-06-20', 'year': '2025', 'genre': '', 'audio_path': 'downloads\\Golden.m4a', 'cover_path': 'downloads\\Golden.jpg', 'MB_album_artist_id': 'dc7fd424-6ba4-45cc-b407-7716c7bb3605', 'MB_album_id': '0028fe3b-409f-4236-9bd7-323076076465', 'MB_other_artist_id': 'def09761-f28a-4486-a796-360d4a4854aa', 'MB_release_group_id': '59f47b29-50dd-4335-a81b-02297c790208', 'MV_album_id': '0028fe3b-409f-4236-9bd7-323076076465', 'MB_track_id': '61f7da88-b161-445b-bc48-8ac574b48dc3'}
    EditTag(song_info)
    
    song = MP4("downloads\\Golden.m4a")
    for k, v in song.tags.items():
        print(f"{k}: {v}")