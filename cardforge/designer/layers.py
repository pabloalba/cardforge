from io import BytesIO

import requests
from PIL import Image, ImageDraw

from .sizes import export_troquel_mini


class Layer:
    def __init__(self, type, enabled=True, x=0, y=0, file=None, font=None, font_size=None, text_align=None,
                 font_weight=None, color=None, text=""):
        self.type = type
        self.enabled = enabled
        self.x = x
        self.y = y
        self.file = file
        self.font = font
        self.font_size = font_size
        self.text_align = text_align
        self.font_weight = font_weight
        self.color = color
        self.text = text


def create_card(size, layers):
    im = Image.new("RGBA", (825, 600))
    draw = ImageDraw.Draw(im)
    for layer in layers:
        if layer.type == "image":
            file = layer.file
            file = file.replace("www.dropbox.com", "dl.dropboxusercontent.com")

            response = requests.get(file)
            image = Image.open(BytesIO(response.content))
            im.paste(image, (layer.x, layer.y), image)
        elif layer.type == "text":
            # font = ImageFont.truetype("sans-serif.ttf", 16)

            draw.text((layer.x, layer.y), layer.text, layer.color)

    im.save("card.png")


if __name__ == "__main__":
    layers = [
        Layer(type="background", color="#FF0000"),
        Layer(type="image", file="https://www.dropbox.com/s/vrpgh14b1kw271s/base.png?dl=0"),
        Layer(type="image", file="https://www.dropbox.com/s/a8aeycs0fqckqfw/circle.png?dl=0"),
        Layer(type="image", file="https://www.dropbox.com/s/00ei8pzgcfsg5p3/paca.png?dl=0"),
        Layer(type="text", font="", font_size=48, color="#00FF00", text="Paca", x=100, y=50),
    ]

    create_card(export_troquel_mini, layers)
