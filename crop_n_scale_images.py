"""crop images of a planet to a tightly-fitting box around the planet."""
import os
import sys
import shutil
from PIL import Image, ImageOps

def get_start_folder():
    """Get name of folder with initial video frames."""
    contents = os.listdir()
    while True:
        frames = input("Name of folder in {} with starting " \
                       "images [default=video_frames]: ".format(os.getcwd()))
        if frames.lower() == 'quit':
            sys.exit()
        elif frames == '':
            frames = 'video_frames'
        if frames not in contents:
            print("Unable to find folder '{}'. Try again or type QUIT to exit."
                  .format(frames), file=sys.stderr)
            continue
        else:
            break
    return frames

def del_folders(name):
    """If a folder exists delete it."""
    contents = os.listdir()
    for item in contents:
        if os.path.isdir(item) and item.startswith(name):
            shutil.rmtree(item)

def clean_folder(prefix_to_save):
    """Delete all files in folder except those with a named prefix."""
    files = os.listdir()
    for file in files:
        if not file.startswith(prefix_to_save):
            os.remove(file)

def crop_images(folder):
    """Automatically crop and scale images of a planet to box around planet."""
    os.chdir(folder)
    files = os.listdir()
    file_num = 1
    for file in files:        
        img = Image.open(file)
        img.load()
        gray = img.convert('L')
        bw = gray.point(lambda x: 0 if x < 90 else 255)
        box = bw.getbbox()       
        padded_box = (box[0]-20, box[1]-20, box[2]+20, box[3]+20)
        cropped = img.crop(padded_box)
        scaled = ImageOps.fit(cropped, (860, 860), Image.LANCZOS, 0, (0.5, 0.5))
        file_name = 'cropped_{}.jpg'.format(file_num)
        scaled.save(file_name, "JPEG")
        file_num += 1
  
def main():
    """Get starting folder, copy folder, run crop function."""
    # get user input
    frames = get_start_folder()

    # prepare files & folders
    del_folders('cropped')
    shutil.copytree(frames, 'cropped')

    # run cropping function
    print("start cropping and scaling...")
    crop_images('cropped')
    clean_folder(prefix_to_save='cropped') # delete uncropped originals
    print("Done! \n")

if __name__ == '__main__':
    main()
