"""Average pairs of images, keeping intermediates in separate folders."""
import os
import sys
import shutil
import math
from PIL import ImageChops, Image

def get_num_pics(path):
    """Return the number of files in a folder."""
    pics = os.listdir(path)
    num_pics = len(pics)
    return num_pics

def confirm_pow2(num_pics):
    """Check that a number is a power of two."""
    return ((num_pics & (num_pics - 1)) == 0) and num_pics != 0

def get_num_dirs(num_pics):
    """Calculate number of new folders needed based on number of images."""
    num_dirs = int(math.log(num_pics, 2))
    return num_dirs

def del_folders(name):
    """If a folder exists delete it."""
    folders = os.listdir()
    for folder in folders:
        if os.path.isdir(folder) and folder.startswith(name):
            shutil.rmtree(folder)

def make_dirs(parent_folder, num_dirs):
    """Make folders to hold combined image pairs."""
    folder_num = 1
    name = 'stack_' 
    while folder_num <= num_dirs:       
        dest = parent_folder + '/' + name + '{}'.format(folder_num)
        if os.path.isdir(dest):
            del_folders(name)
        os.makedirs(dest)
        folder_num += 1

def move_files(folder, dest, prefix):
    """Move files between folders based on a file prefix."""
    os.chdir(folder)
    items = os.listdir()
    for item in items:
        if item.startswith(prefix):
            print("moving {}".format(item)) 
            shutil.move(item, dest)
         
def stack_images(source, dest, num_dirs):
    """Stack images and place each stack in separate folder."""
    folder_num = 1
    file_num = 1
    for folder in range(1, num_dirs + 1):
        os.chdir(source)
        print("current folder = {}".format(source))
        print("destination = {}".format(dest))
        files = os.listdir()
        if len(files) <= 1:
            break
        else: 
            loc_1 = 0
            loc_2 = 1
            while loc_1 < len(files):
                first_image = Image.open(files[loc_1])
                second_image = Image.open(files[loc_2])
                paired_image = ImageChops.add(first_image, second_image,
                                              2, 0)
                prefix = str(folder)
                file_name = '{}file{}.jpg'.format(prefix, file_num)
                paired_image.save(file_name, 'JPEG')
                
                file_num += 1
                loc_1 += 2
                loc_2 += 2
                    
            # move pairs into new folder, change folders, advance file number
            move_files(source, dest, prefix)
            source = dest
            folder_num += 1
            dest = '../stack_{}'.format(folder_num)
            file_num += 1
            
def main():
    """Average series of images, by pairs, using Pillow module."""
    # replace the three paths below with the paths you are using
    # but keep final folder names for source & dest
    top_dir = 'C:\\Python35\\Python 3 Stuff\\Planet Stacking\\for_book'
    source = 'C:\\Python35\\Python 3 Stuff\\Planet Stacking\\for_book\\cropped'
    dest = 'C:\\Python35\\Python 3 Stuff\\Planet Stacking\\for_book\\stack_1'

    os.chdir(top_dir)
    print("current folder = {}".format(os.getcwd()))
    
    num_pics = get_num_pics('./cropped')
    print("num_pics = {}".format(num_pics))
    
    validate_num_pics = confirm_pow2(num_pics)
    if not validate_num_pics:
        print("ERROR: number of images must be a power of 2! Terminating.",
              file=sys.stderr)
        sys.exit(1)        

    num_dirs = get_num_dirs(num_pics)
    print("Number of folders needed = {}".format(num_dirs))
    make_dirs(top_dir, num_dirs)

    stack_images(source, dest, num_dirs)

    print("Done!")

if __name__ == '__main__':
    main()
