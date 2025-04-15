# Libraries
from os import path,listdir
from shutil import move 

# Other Folder
from Mutagen_Tagger import ChangeTag

def GatherInfo():
    
    title = []
    artist = []
    album = []
    track_num = []
    file_extension = []
    cover = []
    
    raw_dir = input("Enter the path to the raw songs directory: ")
    edited_dir = input("Enter the path to the edited songs directory: ")
    cover_dir = input("Enter the path to the cover directory: ")
    
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
        
    return raw_dir, edited_dir, cover_dir, files, file_extension, title, artist, album, track_num, cover
            
def MoveFiles(raw_dir,edited_dir,files):
    for index in range(len(files)):
        try:
            if (artist[index] == ""):
                move(raw_dir+"\\"+files[index],edited_dir+"\\"+title[index]+file_extension[index])
            else:
                move(raw_dir+"\\"+files[index],edited_dir+"\\"+title[index]+" - "+artist[index]+file_extension[index])
        except Exception as e:
            print(e)
        

    

if __name__ == "__main__":
    raw_dir, edited_dir, cover_dir, files, file_extension, title, artist, album, track_num, cover = GatherInfo()
    print("Taging")
    ChangeTag(raw_dir,files,file_extension,title,artist,album,track_num)
    print("Moving Files")
    MoveFiles(raw_dir,edited_dir,files)