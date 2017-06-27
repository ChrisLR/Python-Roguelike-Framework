from PIL import Image, ImageDraw, ImageFont
import os

from data.python_templates.tiles import tiles

width = len(tiles) * 8
height = width
image = Image.new('RGB', (width, height), (255, 255, 255))
font = ImageFont.truetype(os.path.relpath('arial.ttf'), size=16)
image_draw = ImageDraw.Draw(image)
image_path = os.path.dirname(os.path.realpath(__file__)) + 'tileset.png'

x = 0
y = 0
for tile in tiles:
    image_draw.rectangle(((x, y), (x + 16, y + 16)), fill=tile.display.background_color)
    image_draw.text((x, y), tile.display.ascii_character, font=font, fill=tile.display.foreground_color)
    y += 16
    if y >= height:
        if x >= width:
            break
        else:
            y = 0
            x += 16
image.save(image_path)

original_data = {
    "columns": 14,
    "image": "terminal8x8_gs_ro.png",
    "imageheight": 128,
    "imagewidth": 128,
    "margin": 0,
    "name": "terminal8x8_gs_ro",
    "spacing": 1,
    "tilecount": 196,
    "tileheight": 8,
    "tiles":
    {
        "14":
            {
                "type": "t"
            }
    },
     "tilewidth": 8,
     "transparentcolor": "#000000",
     "type": "tileset"
}
