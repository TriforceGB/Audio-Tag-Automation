from GenreChecker import CheckGenre

def AddMissing(song_info: dict) -> dict:
    for key, value in song_info.items():
        if value == "" or value == []:
            if key == "artist" or key == "album_artist" or key == "genre":
                print(f"info missing: {key}")
                newList = []
                while True:
                    newvalue = input("Enter Value or Space to end: ")
                    if newvalue == "":
                        break
                    else: 
                        if key == "genre" and not CheckGenre(newvalue) :
                            continue
                        newList.append(newvalue)
                song_info[key] = newList
            elif key == "audio_path" or key == "cover_path" or key == "cropped_cover_path" or key == 'acoustid':
                pass
            else:
                print(f"info missing: {key}")
                song_info[key] = input(f"Enter Value: ")
    return song_info

def DictPrintout(song_info: dict) -> None:
    for key, value in song_info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    song_info = {'title': '', 'artist': ['HUNTR/X', '이재', 'AUDREY NUNA', 'REI AMI', 'KPop Demon Hunters Cast'], 'album_artist': 'KPop Demon Hunters Cast', 'album': 'KPop Demon Hunters (Soundtrack from the Netflix Film)', 'disc_number': '1', 'total_discs': 1, 'track_number': '6', 'total_tracks': 12, 'release_date': '2025-06-20', 'year': '2025', 'genre': ['k-pop', 'pop'], 'audio_path': 'downloads\\Strategy.m4a', 'cover_path': 'downloads\\Strategy.jpg', 'cropped_cover_path': '', 'MB_album_artist_id': 'dc7fd424-6ba4-45cc-b407-7716c7bb3605', 'MB_album_id': '0028fe3b-409f-4236-9bd7-323076076465', 'MB_other_artist_id': 'def09761-f28a-4486-a796-360d4a4854aa', 'MB_release_group_id': '59f47b29-50dd-4335-a81b-02297c790208', 'MB_release_id': '0028fe3b-409f-4236-9bd7-323076076465', 'MB_track_id': '1d5300eb-2990-481f-b795-dc1da22267f6'}
    AddMissing(song_info)
    