import json
import uuid
from io import BytesIO

import requests
import requests_cache
from PIL import Image, ImageDraw

from .sizes import export_troquel_mini, sizes

requests_cache.install_cache('cardforge_cache')

BLEED = 35
MM_TO_PX = 11.811


def _mm_to_px(mm):
    return int(round(mm * MM_TO_PX))


def forge_deck(deck):
    # Read json
    cards = json.loads(deck.cards)
    front_layers = json.loads(deck.front_layers)
    back_layers = json.loads(deck.front_layers)
    size = deck.size

    forged_cards_fronts, forged_cards_backs = forge_cards(cards, front_layers, back_layers, size, deck.portrait)

    # TODO: Choose export format
    images = weld_cards(export_troquel_mini, forged_cards_fronts, forged_cards_backs)

    file_path = "/tmp/{}.pdf".format(uuid.uuid4())
    # file_path = "/tmp/{}.png".format(uuid.uuid4())

    # Convert images to pdf
    images[0].save(file_path, save_all=True, append_images=images[1:])
    # images[0].save(file_path)

    return file_path


def forge_card_to_png(deck, num_card, front=True):
    # Read json
    cards = json.loads(deck.cards)
    if num_card < len(cards):
        front_layers = json.loads(deck.front_layers)
        back_layers = json.loads(deck.front_layers)
        size = deck.size
        if front:
            im = forge_card(size, front_layers, cards[num_card], deck.portrait)
        else:
            im = forge_card(size, back_layers, cards[num_card], deck.portrait)

        file_path_png = "/tmp/{}.png".format(uuid.uuid4())
        im.save(file_path_png, resoultion=300.0)
        return file_path_png
    return None


def forge_cards(cards, front_layers, back_layers, size, portrait):
    cards_fronts = []
    cards_backs = []

    for card in cards:
        cards_fronts.append(
            forge_card(size, front_layers, card, portrait)
        )
        cards_backs.append(
            forge_card(size, back_layers, card, portrait)
        )

    return cards_fronts, cards_backs

    #
    # return [
    #     "/tmp/naufragio/barracuda.png",
    #     "/tmp/naufragio/barracuda.png",
    #     "/tmp/naufragio/espada.png",
    #     "/tmp/naufragio/espada.png",
    #     "/tmp/naufragio/medusa.png",
    #     "/tmp/naufragio/medusa.png",
    #     "/tmp/naufragio/salazon.png",
    #     "/tmp/naufragio/salazon.png",
    #     "/tmp/naufragio/salazon.png",
    #     "/tmp/naufragio/vendas.png",
    #     "/tmp/naufragio/vendas.png",
    #     "/tmp/naufragio/barril-agua.png",
    #     "/tmp/naufragio/barril-agua.png",
    #     "/tmp/naufragio/barril-agua.png",
    #     "/tmp/naufragio/farol.png",
    #     "/tmp/naufragio/farol.png",
    #     "/tmp/naufragio/morena.png",
    #     "/tmp/naufragio/morena.png",
    #     "/tmp/naufragio/tesoro.png",
    #     "/tmp/naufragio/tesoro.png",
    #     "/tmp/naufragio/barril-rum.png",
    #     "/tmp/naufragio/barril-rum.png",
    #     "/tmp/naufragio/barril-rum.png",
    #     "/tmp/naufragio/herramientas.png",
    #     "/tmp/naufragio/pistola.png",
    #     "/tmp/naufragio/tiburon.png",
    #     "/tmp/naufragio/cana-pescar.png",
    #     "/tmp/naufragio/cana-pescar.png",
    #     "/tmp/naufragio/machete.png",
    #     "/tmp/naufragio/machete.png",
    #     "/tmp/naufragio/pulpo.png",
    #     "/tmp/naufragio/pulpo.png",
    #     "/tmp/naufragio/pulpo.png",
    #     "/tmp/naufragio/tridente.png"
    # ]


def forge_card(size_name, layers, card, portrait):
    size = sizes.get(size_name)
    if portrait:
        im = Image.new("RGBA", (size['HEIGHT_PX'] + 2 * BLEED, size['WIDTH_PX'] + 2 * BLEED))
    else:
        im = Image.new("RGBA", (size['WIDTH_PX'] + 2 * BLEED, size['HEIGHT_PX'] + 2 * BLEED))

    draw = ImageDraw.Draw(im)
    for layer in reversed(layers):
        # mm to pixels
        x = _mm_to_px(layer["x"]) + BLEED
        y = _mm_to_px(layer["y"]) + BLEED

        if layer["type"] == "image":

            file = layer["file"]
            if not file:
                # Read values from cards
                file = card.get("_{}".format(layer["name"]), "")

            if file:
                file = file.replace("www.dropbox.com", "dl.dropboxusercontent.com")
                # TODO: Add cache
                response = requests.get(file)
                image = Image.open(BytesIO(response.content))

                im.paste(image, (x, y), image)
        elif layer["type"] == "text":
            # font = ImageFont.truetype("sans-serif.ttf", 16)
            draw.text((x, y), layer.text, layer.color)

    return im


def weld_cards(export, forged_cards_fronts, forged_cards_backs):
    images = []
    x = export['MARGIN_X']
    y = export['MARGIN_Y']
    num = 0
    rows = 0
    im = Image.new("RGBA", (export['WIDTH'], export['HEIGHT']))

    # TODO: Card backs
    for card in forged_cards_fronts:
        if export['ROTATE']:
            card = card.transpose(Image.ROTATE_270)
        weld_card(export, im, card, x, y)
        x += export['GAP_X'] + export['BOX_WIDTH']
        num += 1
        if num == export['CARDS_PER_ROW']:
            x = export['MARGIN_X']
            y += export['GAP_Y'] + export['BOX_HEIGHT']
            num = 0
            rows += 1
            if rows == export['ROWS']:
                _add_image_to_image_list(im, images)
                im = Image.new("RGBA", (export['WIDTH'], export['HEIGHT']))
                rows = 0
                x = export['MARGIN_X']
                y = export['MARGIN_Y']

    if images == [] or images[-1] != im:
        _add_image_to_image_list(im, images)

    return images


def _add_image_to_image_list(image, image_list):
    rgb = Image.new('RGB', image.size, (255, 255, 255))  # white background
    rgb.paste(image, mask=image.split()[3])  # paste using alpha channel as mask
    image_list.append(rgb)


def weld_card(size, im, card, x, y):
    # draw margin
    # box = (x, y, x + size['BOX_WIDTH'], y + size['BOX_HEIGHT'])
    # im.paste("black", box=box)

    # draw card
    margin_x = int(round((size['BOX_WIDTH'] - card.width) / 2))
    margin_y = int(round((size['BOX_HEIGHT'] - card.height) / 2))
    box = (x + margin_x, y + margin_y)

    im.paste(card, box=box)
    if size['CUT_MARKS']:
        draw_cut_marks(size, im, x, y)


def draw_cut_marks(size, im, x, y):
    draw = ImageDraw.Draw(im)

    # Vertical
    pos_x = x + size['CUT_MARK_DISPLACEMENT']
    pos_y = y + size['CUT_MARK_OVERLAP'] - size['CUT_MARK_SIZE'] - 1
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=True)

    pos_x = x + size['BOX_WIDTH'] - size['CUT_MARK_DISPLACEMENT'] - 1
    pos_y = y + size['CUT_MARK_OVERLAP'] - size['CUT_MARK_SIZE'] - 1
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=True)

    pos_x = x + size['CUT_MARK_DISPLACEMENT']
    pos_y = y + size['BOX_HEIGHT'] - size['CUT_MARK_OVERLAP'] - 1
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=True)

    pos_x = x + size['BOX_WIDTH'] - size['CUT_MARK_DISPLACEMENT'] - 1
    pos_y = y + size['BOX_HEIGHT'] - size['CUT_MARK_OVERLAP'] - 1
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=True)

    # Horizontal
    pos_x = x + size['CUT_MARK_OVERLAP'] - size['CUT_MARK_SIZE'] - 1
    pos_y = y + size['CUT_MARK_DISPLACEMENT']
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=False)

    pos_x = x + size['BOX_WIDTH'] - size['CUT_MARK_OVERLAP'] + 1
    pos_y = y + size['CUT_MARK_DISPLACEMENT']
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=False)

    pos_x = x + size['CUT_MARK_OVERLAP'] - size['CUT_MARK_SIZE'] - 1
    pos_y = y + size['BOX_HEIGHT'] - size['CUT_MARK_DISPLACEMENT'] - 1
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=False)

    pos_x = x + size['BOX_WIDTH'] - size['CUT_MARK_OVERLAP'] + 1
    pos_y = y + size['BOX_HEIGHT'] - size['CUT_MARK_DISPLACEMENT'] - 1
    draw_cut_mark(draw, size, pos_x, pos_y, vertical=False)

    del draw


def draw_cut_mark(draw, size, pos_x, pos_y, vertical=True):
    if vertical:
        draw.line((pos_x, pos_y, pos_x, pos_y + size['CUT_MARK_SIZE'] - 1), fill=(0, 255, 0, 255))
        # draw.line((pos_x + 1, pos_y, pos_x + 1, pos_y + size['CUT_MARK_SIZE'] - 1), fill=(0, 255, 0, 255))
    else:
        draw.line((pos_x, pos_y, pos_x + size['CUT_MARK_SIZE'] - 1, pos_y), fill=(0, 255, 0, 255))
        # draw.line((pos_x, pos_y + 1, pos_x + size['CUT_MARK_SIZE'] - 1, pos_y + 1), fill=(0, 255, 0, 255))
