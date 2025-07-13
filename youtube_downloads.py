from yt_dlp import YoutubeDL
from os import path

# Converts a Playlist URL to a List of URLs
def PlaylistToURL(url:str) -> list[str]:
    ydl_opts = {
        'extract_flat': True,  # Don't download the videos, just get metadata
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        # Extract info dict
        info = ydl.extract_info(url, download=False)
        # The entries contain the videos
        entries = info.get('entries', [])
        # Extract URLs
        playlist_urls = [entry['url'] for entry in entries]
        return playlist_urls

def FetchSongInfo(url: str) -> dict[str]:
    ydl_opts = {
        'extract_flat': True,  # Don't download the videos, just get metadata
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        # Extract info dict
        info = ydl.extract_info(url, download=False)
    fetch_info: dict = {
    'title': info['title'],
    'release_date': f"{info['upload_date'][:4]}-{info['upload_date'][4:6]}-{info['upload_date'][6:]}",
    'year': f"{info['upload_date'][:4]}"
    }
    return fetch_info
# Download Audio from a URL
def DownloadAudio(url: str, output_path: str, filetype='m4a') -> dict[str]: 
    # all the Download Options
    ydl_opts = {
        'final_ext': 'm4a',
        'outtmpl': path.join(output_path,'%(title)s.%(ext)s'),
        'format': 'bestaudio/best',
        'convertthumbnails': 'jpg',
        'writethumbnail': True,
        'windowsfilenames': True,
        'postprocessors': [
            {
                'api': 'https://sponsor.ajay.app',
                'categories': {'music_offtopic'},
                'key': 'SponsorBlock',
                'when': 'after_filter'
            },
            {
                'format': 'jpg',
                'key': 'FFmpegThumbnailsConvertor',
                'when': 'before_dl'
            },
            {
                'key': 'FFmpegExtractAudio',
                'nopostoverwrites': False,
                'preferredcodec': filetype,
                'preferredquality': '5'
            },
            {
                'force_keyframes': False,
                'key': 'ModifyChapters',
                'remove_chapters_patterns': [],
                'remove_ranges': [],
                'remove_sponsor_segments': {'music_offtopic'},
                'sponsorblock_chapter_title': '[SponsorBlock]: '
                                                   '%(category_names)l'
            }
        ],
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        dl_path = path.splitext(ydl.prepare_filename(info))[0]
        ydl.download([url])

        filename = dl_path.split('\\')[-1]
        audio_path=f'{dl_path}.m4a'
        cover_path=f'{dl_path}.jpg'
        
        return filename,audio_path, cover_path
     

if __name__ == "__main__":
    print("YT-DLP Test")
    downloadDir = 'downloads'
    url = input("Enter YouTube video URL: ")
    if url.find("playlist") != -1:
        print("Playlist Detected")
        playlist_urls = PlaylistToURL(url)
        for url in playlist_urls:
            print(DownloadAudio(url, downloadDir))
    else:
        print(DownloadAudio(url, downloadDir))