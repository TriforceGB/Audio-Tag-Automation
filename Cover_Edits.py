from PIL import Image

def crop_cover(cover_path: str, download_path: str) -> str: # Crops to 1:1 Center
    cover = Image.open(cover_path)
    width, height = cover.size
    cutamount=(width-height)/2
    left = cutamount
    top = 0
    right = width-cutamount
    bottom = height
    
    cover_path = download_path+'\\cover.jpg'
    
    cropCover = cover.crop((left,top,right,bottom))
    cropCover.save(cover_path)
    return cover_path
    

if __name__ == '__main__':
    cover = '.\\downloads\\kris_piano_sevenfour - Deltarune Chapter 4.jpg'
    download_dir = ".\\downloads"
    
    crop_cover(cover,download_dir)