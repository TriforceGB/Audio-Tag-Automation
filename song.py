# we would have some class which would be the song class 
# each object would be a new song we wanted to download 
# each object would have a URl for the song at it start point
# we would want to store object in a list or something like that
# also for playlist download we would want it to take the song at a list of url not have it download all the files


# File Imports
from youtube_downloads import FetchSongInfo, DownloadAudio
from acoust_id import GetFingerprint, submitFingerprint
from musicbrainz_fetch import MusicBrainzFetch,SubmitTag,MusicBrainzAlbumCorrection, getCoverImage
from file_management import RenameSong,AlbumFolder,MoveSong,RemoveCover
from cover_crop import CropCover
from tagger import ManualAddTag,EditTag
class song:
    def __init__(self, url:str):
        self.url: str = url
        self.fingerprint: str
        self.duration: int
        self.filename: str
        self.audio_path: str
        self.cover_path: str
        self.cropped_cover_path: str
        self.album_folder: str
        self.song_info: dict = {
                                'title': "",
                                'sort_title': "",
                                'original_title': "",
                                'artist': [],
                                'album_artist': [],
                                'album': "",
                                'disc_number': "",
                                'total_discs': "",
                                'track_number':"",
                                'total_tracks': "",
                                'release_date': "",
                                'year': "",
                                'genre': [], 
                                'MB_album_artist_id': "",
                                'MB_album_id': "",
                                'MB_other_artist_id': "", 
                                'MB_release_group_id': "",
                                'MB_track_id': "",
                                'AcoustID': ""
                                }
    # Prints all the Info on Song Info 
    def print_info(self) -> None:
        for k, v in self.song_info.items():
            print(f"{k}: {v}")
    # Manually edits song info if they are missing
    def manual_edit(self, ManualTagging:bool) -> bool:
        self.print_info()
        ManualTagging_info, ChangeMade = ManualAddTag(self.song_info,ManualTagging)
        self.song_info.update(ManualTagging_info)
        return ChangeMade
        
    # Fetches Song Info From Youtube
    def youtube_fetch(self) -> str:
        fetch_info = FetchSongInfo(self.url)
        self.song_info.update(fetch_info)
        return self.song_info['title']
        
    # Downloads Song From Youtube
    def youtube_download(self, DownloadDir:str) -> str:
        self.filename,self.audio_path,self.cover_path = DownloadAudio(self.url,DownloadDir)
        return self.audio_path
    
    # Get Fingerprint, RID, and AcoustID
    def acoustid_fingerprint(self,ACOUSTID_APP_API:str,ManualIntervention:bool) -> str:
        acoustid_info, self.fingerprint, self.duration = GetFingerprint(self.audio_path,ACOUSTID_APP_API,ManualIntervention)
        self.song_info.update(acoustid_info)
        return self.fingerprint, self.duration
    # Submit Fingerprint Back to the DB
    def acoustid_submit_fingerprint(self, ACOUSTID_APP_API: str, ACOUSTID_USER_API: str) -> None:
        submitFingerprint(ACOUSTID_APP_API, ACOUSTID_USER_API, self.fingerprint,self.duration,self.song_info)
    
    # Uses Recording ID to get all the MetaData
    def musicbrainz_search(self, ManualIntervention:bool) -> None:
        MusicBrainz_info = MusicBrainzFetch(self.song_info['MB_track_id'],ManualIntervention)
        self.song_info.update(MusicBrainz_info)
    # Edit the Album info to match the main Album
    def musicbrainz_album_correction(self, FirstSong_Info:dict) -> None:
        updated_info = MusicBrainzAlbumCorrection(self.song_info,FirstSong_Info)
        self.song_info.update(updated_info)
    # Submits Added Edits to the DB
    def musicbrainz_submit(self) -> None:
        SubmitTag(self.song_info['MB_track_id'],self.song_info['genre'])
    
    def cover(self,DownloadDir:str,ManualTagging:bool,ManualIntervention:bool) -> str:
        # If to Use Which Cover (Only when Manual Tagging)
        if ManualTagging == True or ManualIntervention == True: 
            if input("Use MusicBrainz Cover? (y/n): ").lower() == "n":
                UseMusicBrainzCover = False
            else:
                UseMusicBrainzCover = True
        else:
            UseMusicBrainzCover = True
        if UseMusicBrainzCover == True:
            getCoverImage(self.song_info['MB_album_id'],self.cover_path)
        self.cropped_cover_path = CropCover(self.cover_path,DownloadDir)
        
    def add_tags(self) -> None:
        EditTag(self.song_info,self.audio_path,self.cropped_cover_path)

    def rename_song(self,DownloadDir:str) -> None:
        self.filename,self.audio_path = RenameSong(self.audio_path,DownloadDir,self.song_info['title'],self.song_info['album_artist'])
    def create_album_folder(self,MusicDir:str) -> None:
        self.album_folder = AlbumFolder(MusicDir,self.song_info['album'])
    def move_song(self) -> None:
        MoveSong(self.audio_path,self.album_folder,self.filename)
    def remove_cover(self) -> None:
        RemoveCover(self.cover_path,self.cropped_cover_path)