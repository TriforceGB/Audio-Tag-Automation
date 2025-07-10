from yt_dlp import YoutubeDL
from os import path

def download_audio(url: str, output_path: str, filetype='m4a') -> str: 
    # Used to Download Audio from Youtube
    # 
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
        filename = path.splitext(ydl.prepare_filename(info))[0]
        print(filename)
        ydl.download([url])
        
        
        dl_info: dict = {
            'audio_path':f'{filename}.m4a',
            'cover_path':f'{filename}.jpg',
            'title': info['title'],
            'release_date': f"{info['upload_date'][:4]}-{info['upload_date'][4:6]}-{info['upload_date'][6:]}",
            'year': f"{info['upload_date'][:4]}"
        }
        return dl_info
     

if __name__ == "__main__":
    print("Download Test")
    url = input("Enter YouTube video URL: ")
    print(download_audio(url, 'downloads'))
    

# This need to output:
 # Path of Audio
 # Path of Thumbnail
 # Title
 # Release Date