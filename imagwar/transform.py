from wand.image import Image
from wand.display import display

with Image(filename='mycv.pdf') as img:
    print(img.size)
    for r in range(1,2):
        with img.clone() as i:
            # i.compression_quality = 95
            i.resize(int(450), int(450))
            # i.rotate(90 * r)
            # i.compression_quality = 50
            i.save(filename='cv.jpg'.format(r))
            # display(i)
