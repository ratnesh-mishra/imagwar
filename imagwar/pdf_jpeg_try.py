from wand.image import Image
from wand.color import Color
import os, os.path, sys
all_pages = Image(filename='sample.pdf', resolution=100)
for i, page in enumerate(all_pages.sequence):
        with Image(page) as img:
            img.format = 'png'
            img.background_color = Color('white')
            img.alpha_channel = 'remove'
            img.save(filename='image{}.png'.format(i))
