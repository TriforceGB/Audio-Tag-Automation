#  Auto-Audio-Tagger-Inator-3000
###  NOTE Currently Still in a Work in Progress
The Auto Audio Tagger Inator 3000 is a python project that take youtube links or playlist and uses AcoustID and MusicBrainz DB in order to identify and tag audio.
## Features

- Using yt-dlp to download any video into audio file (default is m4a but could be edited to mp3 or other format with FFMPEG)
- Using AcoustID, it create a fingerprint of audio to find the MBID
    - If it's unable to identify ID it will ask for manual input 
- With the MusicBrainz API it will tag and rename the file for usage in mediaserver or spotify
- Download are set via a Json file with URL to every video and settings that can changed how it is downloaded and tagged


### Download Settings
| Setting      | Description      |
| ------------- | ------------- |
| Name | Nothing it just help for organizing |
| ManualTagging | Skip AcoustID and MusicBrainz and make every song have to be tag Manually |
| ManualIntervention | If true, will ask for input when facted with an issue, if false, will either skip or take first choice without asking |
| MatchingAlbum | Will make sure each song in the download are in the same album (Has issue  if MB has 2 ID for the  same song) |
| StartingInfo | only need to exist if Matching Album is enable, act as the first download song and tell every other song to use this info of album ID and Album Artist |
|ManualID | if enable, will not go  to AcoustID and just ask for The MBID |
| SubmitToDB |  Will Submit info such as fingerprints or tag to AcoustID or MB |
| AddGenre | If it should try to add Genre Tag (MB doesn't have most song with this Tag) |


## Setup
Currently to run this you need setup a few other software and API keys to work
### Software
For the Tagger to work you need a few other software either in the directory or in your path environment variable
#### List of Software
- [ffmpeg](https://ffmpeg.org/)
- [chromaprint](https://acoustid.org/chromaprint)
### API
The Tagger also depends on having access to both MusicBrainz and AcoustID API / Accounts that it looks for in Environment Variables

The AcoustID API can be found on the Links after making an Account. The MusicBrainz Info is just your Account info
#### List of API
- [ACOUSTID_APP_API](https://acoustid.org/new-application)
- [ACOUSTID_USER_API](https://acoustid.org/api-key)
- [MUSICBRAINZ_USER](https://musicbrainz.org/)
- [MUSICBRAINZ_PASS](https://musicbrainz.org/)
## Usage
Once the API are Setup you want to setup your download.json by using the download_example.json or the json below

generally most download should like the first example is for most download, the 2nd example is when you have MatchingAlbum enable
```json
    "DownloadDir": "\\Path\\To\\Temp\\Download\\Storage",
    "MusicDir": "\\Path\\To\\Stored\\Music",
    "Groups": [
        {
            "Name": "Group Name Goes Here",
            "ManualTagging": false,
            "ManualIntervention": true,
            "MatchingAlbum": false,
            "ManualID": false,
            "SubmitToDB": true,
            "AddGenre": false,
            "URLs": [
                "Youtube Link to Playlist/Songs Goes Here",
                "Youtube Link to Playlist/Songs Goes Here",
                "Youtube Link to Playlist/Songs Goes Here"
            ]
        },
        {
            "Name": "Group Name Goes Here",
            "ManualTagging": false,
            "ManualIntervention": true,
            "MatchingAlbum": true,
            "ManualID": false,
            "SubmitToDB": true,
            "AddGenre": false,
            "Starting_Info": {
                "MB_album_id": "album_id Goes Here",
                "album_artist": [
                    "Album Artist Names Goes Here"
                ]
            },
            "URLs": [
                "Youtube Link to Playlist/Songs Goes Here"
            ]
        }
    ]
```
## Todo
As mention This project is far from done however it in a place that is useable for me to download stuff. On the Todo List we have
- Make a WebUI
- Turn this into a Docker Image and have it be able to run of something like a home server
- Have it be more consistent with picking the right album
- refactor all the code for it not to be crap
