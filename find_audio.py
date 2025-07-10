from acoustid import lookup,fingerprint_file,submit


# for score, recording_id, title, artist in :
#     print(score,recording_id,title,artist)

def findRID(path: str, AppAPI: str, takeTop: bool) -> str:
    duration, fingerprint = fingerprint_file(path)
    print(duration, fingerprint)
    lookup_data = lookup(AppAPI, fingerprint, duration)
    if len(lookup_data['results']) > 1 and not takeTop:
        print("more then 1 Match Found Pick which one you want")
        count=0
        for result in lookup_data['results']:
            print(f"{count}) {result['title']}, {result['id']}")
            count =+ 1
        while True:
            try: 
                correctSong = int(input("Select the Song you Want: "))-1
                break
            except Exception as e:
                print(e)
        rid = lookup_data['results'][correctSong]['recordings'][correctSong]['id']
    else:
        rid = lookup_data['results'][0]['recordings'][0]['id']
    return rid

def submitFingerprint():
    pass #TODO

if __name__ == "__main__":
    path = "Done\\KPop Demon Hunters (Soundtrack from the Netflix Film)\\Takedown-KPop Demon Hunters Cast.m4a"
    takeTop = False
    print(findRID(path,AppAPI,takeTop))

# test = {
#     'results': 
#     [
#         {
#             'id': '78bdbaab-bb9e-4c8f-b052-d7b96bf134a7', 
#             'recordings': 
#             [
#                 {
#                     'artists': 
#                     [
#                         {
#                             'id': '8eeb59f4-0071-4261-b1f8-91d8294622d2', 
#                             'name': '星街すいせい'
#                         }
#                     ], 
#                 'duration': 301.453, 
#                 'id': '32d6ffe7-6285-46a5-b9f6-7dae09824568', 
#                 'title': 'Stellar Stellar'
#                 }
#             ], 
#             'score': 0.9839794
#         }, 
#         {
#             'id': '1bde8ee2-fcc0-4e58-b383-30c6f8d86cc5', 
#             'recordings': 
#             [
#                 {
#                     'artists': 
#                     [
#                         {
#                             'id': '8eeb59f4-0071-4261-b1f8-91d8294622d2', 
#                             'name': '星街すいせい'
#                         }
#                     ], 
#                     'duration': 301.453, 
#                     'id': '32d6ffe7-6285-46a5-b9f6-7dae09824568', 
#                     'title': 'Stellar Stellar'
#                      }
#             ], 
#             'score': 0.7456158
#         }
#     ], 
#     'status': 'ok'
# }

print(len(test['results']))