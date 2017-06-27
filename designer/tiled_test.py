from PIL import Image, ImageDraw, ImageFont
import os
import json

from data.python_templates.tiles import tiles

width = len(tiles) * 8
height = width
image = Image.new('RGB', (width, height), (255, 255, 255))
font = ImageFont.truetype(os.path.relpath('arial.ttf'), size=16)
image_draw = ImageDraw.Draw(image)
folder_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(folder_path, 'tileset.png')
json_path = os.path.join(folder_path, 'tileset.json')

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

new_data = {
    "columns": 14,
    "image": "tileset.png",
    "imageheight": image.height,
    "imagewidth": image.width,
    "margin": 0,
    "name": "Tiles",
    "spacing": 0,
    "tilecount": len(tiles),
    "tileheight": 16,
    "tiles":
    {
        "14":
            {
                "type": "t"
            }
    },
     "tilewidth": 16,
     "type": "tileset"
}

with open(json_path, 'w') as json_file:
    json.dump(new_data, json_file)
