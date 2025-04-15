from taglib import File as Tag
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
        with Tag(raw_dir+"\\"+files[index]) as song:
            song.tags["TITLE"] = title[index]
            song.tags["ARTIST"] = artist[index]
            song.tags["ALBUM"] = album[index]
            song.tags["TRACKNUMBER"] = track_num[index]
            song.save()

def MoveFiles(raw_dir,edited_dir,files):
    for index in range(len(files)):
        if (artist[index] == ""):
            move(raw_dir+"\\"+files[index],edited_dir+"\\"+title[index]+file_extension[index])
        else:
            move(raw_dir+"\\"+files[index],edited_dir+"\\"+title[index]+" - "+artist[index]+file_extension[index])
        

    

if __name__ == "__main__":
    GatherInfo()
    ChangeTag(raw_dir,files,title,artist,album,track_num)
    MoveFiles(raw_dir,edited_dir,files)
        

    
        
