import os
import glob
import ntpath
import zipfile
from lorem.text import TextLorem
from PIL import Image, ImageFont, ImageDraw

for zip in glob.glob('./fonts/dafonts/*.zip'):
    try:
        with zipfile.ZipFile(zip, 'r') as zip_ref:
            zip_ref.extractall('./fonts/extracted/')
    except: ""

fonts = [f for f in glob.glob('./fonts/extracted/*.*f') if ".otf" in f or '.ttf' in f or '.woff' in f]

IMAGE_DIR = './images'

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

lorem = TextLorem(ssep="\n")

print(lorem.paragraph())

for f in fonts:
    print(f)
    name = ' '.join(ntpath.basename(f).split('.')[:-1])
    text = lorem.paragraph()
    font_size = 36
    color = (0, 0, 0)

    font = ImageFont.FreeTypeFont(f, size=font_size)

    img_size = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text=text, font=font)[2:] # connard
    img = Image.new("RGBA", img_size, color=(255, 255, 255))

    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font, fill='black')

    img.save(f"{IMAGE_DIR}/{name}.png")
