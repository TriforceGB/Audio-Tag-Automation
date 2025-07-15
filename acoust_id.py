from acoustid import lookup,fingerprint_file,submit

def GetFingerprint(path: str, AppAPI: str, ManualIntervention: bool) -> dict:
    duration, fingerprint = fingerprint_file(path)
    lookup_data = lookup(AppAPI, fingerprint, duration)
    print(lookup_data)
    if len(lookup_data['results']) > 1 and ManualIntervention:
        print("more then 1 Match Found Pick which one you want")
        count=1
        for result in lookup_data['results']:
            print(f"{count}) {result['recordings'][0]['title'] if 'title' in result['recordings'][0] else 'Unknown Name'}, {result['recordings'][0]['id'] if 'id' in result['recordings'][0] else 'Unknown ID'}") # Takes the first Recording Title
            count += 1
        while True:
            try: 
                correctSong = int(input("Select the Song you Want: "))-1
                break
            except Exception as e:
                print(e)
        rid = lookup_data['results'][correctSong]['recordings'][correctSong]['id']
        acoustid = lookup_data['results'][correctSong]['id']
        
    elif len(lookup_data['results']) == 0:
        print("No Match Found")
        print("Either Enter Recording ID Manually or Press Enter to Enter The Tag Manually")
        rid = input("Recording ID: ")
        acoustid = ""
    else:
        print()
        rid = lookup_data['results'][0]['recordings'][0]['id']
        acoustid = lookup_data['results'][0]['id']
        
    acoustid_info: dict = {
        'AcoustID': acoustid,
        'MB_track_id': rid,
    } 
    return acoustid_info, fingerprint, duration

def submitFingerprint(ACOUSTID_APP_API: str, ACOUSTID_USER_API: str, fingerprint: str, duration: int, song_info: dict) -> None:
    submit(ACOUSTID_APP_API,ACOUSTID_USER_API, {
        'fingerprint': fingerprint,
        'duration': duration,
        'mbid': song_info['MB_track_id'],
        'title': song_info['original_title']
    })

if __name__ == "__main__":
    path = "Done\\KPop Demon Hunters (Soundtrack from the Netflix Film)\\Soda Pop - KPop Demon Hunters Cast.m4a"
    ManualIntervention = False
    from os import getenv
    ACOUSTID_USER_API=getenv('ACOUSTID_USER_API')
    ACOUSTID_APP_API=getenv('ACOUSTID_APP_API')
    print(GetFingerprint(path,ACOUSTID_APP_API,ManualIntervention))
    