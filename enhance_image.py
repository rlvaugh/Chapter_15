"""Run Pillow image enhancement filters on an image & save results."""
import os
import sys
from PIL import Image, ImageFilter, ImageEnhance

def get_path():
    """Get path and name of image to enhance."""
    while True:
        folder = input("Name of folder containing image else QUIT to exit: ")
        if folder.lower() == 'quit':
            sys.exit()
        file = input("Name of image file, with extension: ")
        path = os.path.join('.', folder, file)
        if os.path.exists(path):
            return path
        else:
            print("Invalid path {}.".format(path), file=sys.stderr)
            continue

def enhance_image(image):
    """Improve an image using Pillow filters & transforms."""
    enhancer = ImageEnhance.Brightness(image)
    img_enh = enhancer.enhance(0.75)  # 0.75 looks good
    
    enhancer = ImageEnhance.Contrast(img_enh)
    img_enh = enhancer.enhance(1.6)

    enhancer = ImageEnhance.Color(img_enh)
    img_enh = enhancer.enhance(1.7)

    img_enh = img_enh.rotate(angle=133, expand=True)

    img_enh = img_enh.filter(ImageFilter.SHARPEN)

    return img_enh


def main():
    """Get an image and enhance, show and save it."""
    path = get_path()
    img = Image.open(path)  
    img_enh = enhance_image(img)
    img_enh.show()    
    img_enh.save('enhanced.tif', 'TIFF')

if __name__ == '__main__':
    main()
