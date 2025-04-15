from mutagen.mp4 import MP4, MP4Cover
from mutagen.mp3 import MP3

def ChangeTag(raw_dir,files,file_extension,title,artist,album,track_num):
    for index in range(len(files)):
        try:
            # For .m4a
            if file_extension[index] == '.m4a':  
                song = MP4(raw_dir+"\\"+files[index])

                song["\xa9nam"] = title[index]
                song["\xa9ART"] = artist[index]
                song["\xa9alb"] = album[index]
                if track_num[index] != "":
                    song["trkn"] = [(int(track_num[index]),0)]
                else: 
                    del song["trkn"]
                
                song.save()
            elif file_extension[index] == '.mp3':
                song = MP3(raw_dir+"\\"+files[index])

                song["TIT2"] = title[index]
                song["TPE1"] = artist[index]
                song["TALB"] = album[index]
                song["TRCK"] = track_num[index]
                
                song.save()
            else:
                print("File Extension Not Recognized: ",file_extension[index])
        except Exception as e:
            print(e)