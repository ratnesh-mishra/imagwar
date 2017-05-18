from wand.image import Image
from wand.color import Color
import os, os.path, sys

def pdf2jpg(source_file, target_file, dest_width, dest_height):
    RESOLUTION    = 300
    ret = True
    try:
        with Image(filename=source_file, resolution=(RESOLUTION,RESOLUTION)) as img:
            img.background_color = Color('white')
            img_width = img.width
            ratio     = dest_width / img_width
            img.resize(dest_width, int(ratio * img.height))
            img.format = 'jpeg'
            img.alpha_channel= False
            img.save(filename = target_file)
    except Exception as e:
        print(str(e))
        ret = False

    return ret

if __name__ == "__main__":
    source_file = "dvc.pdf"
    target_file = "cvd.jpg"

    ret = pdf2jpg(source_file, target_file, 1895, 1080)
