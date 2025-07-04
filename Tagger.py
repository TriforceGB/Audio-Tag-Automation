from mutagen.mp4 import MP4, MP4Cover, MP4FreeForm

def EditTag(song_info: dict) -> None:
    with open(song_info['cover_path'], 'rb') as f:
        cover_data = f.read()
        cover = MP4Cover(cover_data,imageformat=MP4Cover.FORMAT_JPEG)
    song = MP4(song_info['audio_path'])
    song["\xa9nam"] = song_info['title']
    song["\xa9ART"] = song_info['artist']
    song["aART"] = song_info['album_artist']
    song["\xa9alb"] = song_info['album']
    song["disk"] = [(int(song_info['disc_number']), int(song_info['total_discs']))] 
    song["trkn"] = [(int(song_info['track_number']), int(song_info['total_tracks']))]
    song["\xa9day"] = song_info['release_date']
    # song["\xa9day"] = song_info['year']
    song["\xa9gen"] = song_info['genre']
    song["----:com.apple.iTunes:MUSICBRAINZ_ALBUMARTISTID"] = MP4FreeForm(song_info['MB_album_artist_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_ALBUMID"] = MP4FreeForm(song_info['MB_album_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_ARTISTID"] = MP4FreeForm(song_info['MB_other_artist_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_RELEASEGROUPID"] = MP4FreeForm(song_info['MB_release_group_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_RELEASETRACKID"] = MP4FreeForm(song_info['MB_release_id'].encode('utf-8'))
    song["----:com.apple.iTunes:MUSICBRAINZ_TRACKID"] = MP4FreeForm(song_info['MB_track_id'].encode('utf-8'))
    song["covr"] = [cover]
    song.save()
    
if __name__ == "__main__":
    song_info = {'title': 'Golden', 'file-name': 'Golden', 'artist': 'HUNTR/X;이재;AUDREY NUNA;REI AMI;KPop Demon Hunters Cast', 'album_artist': 'KPop Demon Hunters Cast', 'album': 'KPop Demon Hunters (Soundtrack from the Netflix Film)', 'disc_number': '1', 'total_discs': 1, 'track_number': '4', 'total_tracks': 12, 'release_date': '2025-06-20', 'year': '2025', 'genre': '', 'audio_path': 'downloads\\Golden.m4a', 'cover_path': 'downloads\\Golden.jpg', 'MB_album_artist_id': 'dc7fd424-6ba4-45cc-b407-7716c7bb3605', 'MB_album_id': '0028fe3b-409f-4236-9bd7-323076076465', 'MB_other_artist_id': 'def09761-f28a-4486-a796-360d4a4854aa', 'MB_release_group_id': '59f47b29-50dd-4335-a81b-02297c790208', 'MB_release_id': '0028fe3b-409f-4236-9bd7-323076076465', 'MB_track_id': '61f7da88-b161-445b-bc48-8ac574b48dc3'}
    EditTag(song_info)
    
    song = MP4("downloads\\Golden.m4a")
    for k, v in song.tags.items():
        print(f"{k}: {v}")