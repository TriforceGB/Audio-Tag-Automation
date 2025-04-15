from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from os import path,listdir
from shutil import move 

raw_dir = ""
edited_dir = ""

files = []
file_extension = []
title = []
artist = []
album = []
track_num = []

def GatherInfo():
    global raw_dir
    global edited_dir
    
    global files
    global file_extension
    global title 
    global artist
    global album
    global track_num
    
    raw_dir = input("Enter the path to the raw songs directory: ")
    edited_dir = input("Enter the path to the edited songs directory: ")
    
    if (input(" Use the Same album for all songs? (y/n) ") == "y"):
        all_album = input("Enter the album of the song: ")
        use_same_album = True
    else:
        use_same_album = False
    
    files = listdir(raw_dir)
    
    for file in files:
        print("For File Called: ",file)
        
        input_title = input("Enter the title of the song: ")
        if input_title != "":
            title.append(input_title)
        else:
            title.append(path.splitext(file)[0])
        artist.append(input("Enter the artist of the song: "))
        
        if (use_same_album):
            album.append(all_album)
        else:
            album.append(input("Enter the album of the song: "))
            
        track_num.append(input("Enter the track number of the song: "))
        file_extension.append(path.splitext(file)[1])

        print("====================================")

def ChangeTag(raw_dir,files,title,artist,album,track_num):
    for index in range(len(files)):
        # For .m4a
        if file_extension[index] == '.m4a':  
            song = MP4(raw_dir+"\\"+files[index])

            song["\xa9nam"] = title[index]
            song["\xa9ART"] = artist[index]
            song["\xa9alb"] = album[index]
            song["trkn"] = [(int(track_num[index]),0)]
            
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

def MoveFiles(raw_dir,edited_dir,files):
    for index in range(len(files)):
        if (artist[index] == ""):
            move(raw_dir+"\\"+files[index],edited_dir+"\\"+title[index]+file_extension[index])
        else:
            move(raw_dir+"\\"+files[index],edited_dir+"\\"+title[index]+" - "+artist[index]+file_extension[index])
        

    

if __name__ == "__main__":
    GatherInfo()
    print("Taging")
    ChangeTag(raw_dir,files,title,artist,album,track_num)
    print("Moving Files")
    MoveFiles(raw_dir,edited_dir,files)
        

    
        
