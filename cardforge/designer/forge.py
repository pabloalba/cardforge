import json
import math
import os
import re
import uuid
from io import BytesIO

import requests
import requests_cache
from PIL import Image, ImageDraw, ImageFont

from .sizes import exports, sizes

requests_cache.install_cache('cardforge_cache')

BLEED = 35
CUT_MARKS_SIZE = 65
GROW = round(CUT_MARKS_SIZE - BLEED / 2)
MM_TO_PX = 11.811


def _mm_to_px(mm):
    return int(round(float(mm) * MM_TO_PX))


def _get_tmp_path(deck):
    tmp_path = "/tmp/cardforge/{}".format(deck.id)
    os.makedirs(tmp_path, exist_ok="true")
    return tmp_path


def forge_deck(deck, export_type, export_format='pdf', export_target='standard'):
    tmp_path = _get_tmp_path(deck)
    # Read json
    cards = json.loads(deck.cards)
    front_layers = json.loads(deck.front_layers)
    back_layers = json.loads(deck.back_layers)
    size = deck.size

    forged_cards_fronts, forged_cards_backs = forge_cards(cards, front_layers, back_layers, size, deck)

    if export_target == 'tabletop':
        images = weld_cards_tabletop(forged_cards_fronts, forged_cards_backs, deck.portrait)
    elif export_target == 'print_and_play':
        images = weld_cards_print_and_play(exports[export_type], forged_cards_fronts, forged_cards_backs,
                                           deck.portrait)
    else:
        images = weld_cards_standard(exports[export_type], forged_cards_fronts, forged_cards_backs)

    if export_format == 'pdf':
        file_path = "{}/{}.pdf".format(tmp_path, uuid.uuid4())
        images[0].save(file_path, save_all=True, append_images=images[1:])
    else:
        # TODO: Zip multiimage
        file_path = "{}/{}.png".format(tmp_path, uuid.uuid4())
        images[0].save(file_path)

    return file_path


def forge_card_to_png(deck, num_card, front=True):
    tmp_path = _get_tmp_path(deck)
    # Read json
    cards = json.loads(deck.cards)
    card = None
    if num_card < len(cards):
        card = cards[num_card]

    front_layers = json.loads(deck.front_layers)
    back_layers = json.loads(deck.back_layers)
    size = deck.size
    if front:
        im = forge_card(size, front_layers, card, deck)
    else:
        im = forge_card(size, back_layers, card, deck)

    file_path_png = "{}/{}.png".format(tmp_path, uuid.uuid4())
    im.save(file_path_png, resoultion=300.0)
    return file_path_png


def forge_cards(cards, front_layers, back_layers, size, deck):
    cards_fronts = []
    cards_backs = []

    for card in cards:
        cards_fronts.append(
            forge_card(size, front_layers, card, deck)
        )
        cards_backs.append(
            forge_card(size, back_layers, card, deck)
        )

    return cards_fronts, cards_backs


def forge_card(size_name, layers, card, deck):
    tmp_path = _get_tmp_path(deck)
    size = sizes.get(size_name)
    if deck.portrait:
        im = Image.new("RGBA", (size['HEIGHT_PX'] + 2 * BLEED, size['WIDTH_PX'] + 2 * BLEED))
    else:
        im = Image.new("RGBA", (size['WIDTH_PX'] + 2 * BLEED, size['HEIGHT_PX'] + 2 * BLEED))

    draw = ImageDraw.Draw(im)
    for layer in reversed(layers):

        if not layer.get("visible", True):
            continue

        # mm to pixels
        x = _mm_to_px(layer["x"]) + BLEED
        y = _mm_to_px(layer["y"]) + BLEED

        if layer["type"] == "image":
            file = None
            if layer["template"]:
                # Read values from layer
                file = layer["file"]
            else:
                # Read values from cards
                file = None
                if card:
                    file = card.get("_{}".format(layer["id"]), "")
            if file:
                response = _download(file)
                image = Image.open(BytesIO(response.content))
                try:
                    im.paste(image, (x, y), image)
                except ValueError:
                    im.paste(image, (x, y))
        elif layer["type"] == "text":
            font_size = int(layer.get("font_size", "32"))

            font_file = layer.get("font", "")
            if font_file:
                safe_font_file = re.sub('[^0-9a-zA-Z]+', '_', font_file)
                file_path_ttf = "{}/{}.ttf".format(tmp_path, safe_font_file)
                if not os.path.isfile(file_path_ttf):
                    response = _download(font_file)
                    ttf = open(file_path_ttf, 'wb')
                    ttf.write(response.content)
                    ttf.close()
            else:
                file_path_ttf = "{}/templates/fonts/Alegreya-Bold.ttf".format(
                    os.path.realpath(os.path.dirname(__file__)))
            font = ImageFont.truetype(file_path_ttf, font_size)

            text = None
            if layer["template"]:
                # Read values from layer
                text = layer["text"]
            else:
                # Read values from cards
                if card:
                    text = card.get("_{}".format(layer["id"]), "")

            if text:
                color = layer.get("color", "#000000")
                draw.text((x, y), text, color, font=font)

    return im


def _download(url):
    url = url.replace("www.dropbox.com", "dl.dropboxusercontent.com")
    return requests.get(url)


def add_cut_marks(original_im):
    if original_im:
        im = Image.new("RGBA", (original_im.width + 2 * GROW, original_im.height + 2 * GROW))

        # draw original card in center
        box = (GROW, GROW)

        im.paste(original_im, box=box)

        draw = ImageDraw.Draw(im)

        # Vertical
        pos_x = GROW + BLEED
        pos_y = 0
        draw.line((pos_x, pos_y, pos_x, pos_y + CUT_MARKS_SIZE), fill=(0, 255, 0, 255))

        pos_x = GROW + BLEED
        pos_y = im.height - CUT_MARKS_SIZE
        draw.line((pos_x, pos_y, pos_x, pos_y + CUT_MARKS_SIZE), fill=(0, 255, 0, 255))

        pos_x = im.width - GROW - BLEED
        pos_y = 0
        draw.line((pos_x, pos_y, pos_x, pos_y + CUT_MARKS_SIZE), fill=(0, 255, 0, 255))

        pos_x = im.width - GROW - BLEED
        pos_y = im.height - CUT_MARKS_SIZE
        draw.line((pos_x, pos_y, pos_x, pos_y + CUT_MARKS_SIZE), fill=(0, 255, 0, 255))

        # Horizontal
        pos_x = 0
        pos_y = GROW + BLEED
        draw.line((pos_x, pos_y, pos_x + CUT_MARKS_SIZE, pos_y), fill=(0, 255, 0, 255))

        pos_x = im.width - CUT_MARKS_SIZE
        pos_y = GROW + BLEED
        draw.line((pos_x, pos_y, pos_x + CUT_MARKS_SIZE, pos_y), fill=(0, 255, 0, 255))

        pos_x = 0
        pos_y = im.height - GROW - BLEED
        draw.line((pos_x, pos_y, pos_x + CUT_MARKS_SIZE, pos_y), fill=(0, 255, 0, 255))

        pos_x = im.width - CUT_MARKS_SIZE
        pos_y = im.height - GROW - BLEED
        draw.line((pos_x, pos_y, pos_x + CUT_MARKS_SIZE, pos_y), fill=(0, 255, 0, 255))

        del (draw)

        return im
    return None


def calculate_margins(export, card):
    max_items_by_row = math.floor(export['WIDTH'] / card.width)
    margin_x = round((export['WIDTH'] - max_items_by_row * card.width) / (max_items_by_row + 1))

    while margin_x < BLEED:
        max_items_by_row -= 1
        margin_x = round((export['WIDTH'] - max_items_by_row * card.width) / (max_items_by_row + 1))

    max_items_by_column = math.floor(export['HEIGHT'] / card.height)
    margin_y = round((export['HEIGHT'] - max_items_by_column * card.height) / (max_items_by_column + 1))

    while margin_y < BLEED:
        max_items_by_column -= 1
        margin_y = round(
            (export['HEIGHT'] - max_items_by_column * card.height) / (max_items_by_column + 1))

    return margin_x, margin_y, max_items_by_row, max_items_by_column


def weld_cards_tabletop(forged_cards_fronts, forged_cards_backs, portrait):
    max_items_by_row = 10
    max_items_by_column = 7
    card = forged_cards_fronts[0]
    if portrait:
        card = card.transpose(Image.ROTATE_270)
    im = Image.new("RGBA", (card.width * max_items_by_row, card.height * max_items_by_column))
    x = 0
    y = 0
    num = 0
    row = 0
    for card in forged_cards_fronts:
        num += 1
        if num < 70:
            if portrait:
                card = card.transpose(Image.ROTATE_270)
            im.paste(card, box=(x, y))
            x += card.width
            row += 1
            if row == max_items_by_row:
                x = 0
                y += card.height
                row = 0

    # Add back on the 70th position
    card = forged_cards_backs[0]
    if portrait:
        card = card.transpose(Image.ROTATE_270)

    im.paste(card, box=(card.width * (max_items_by_row - 1), card.height * (max_items_by_column - 1)))

    images = []
    _add_image_to_image_list(im, images)
    return images


def weld_cards_print_and_play(export, forged_cards_fronts, forged_cards_backs, portrait):
    # Join front and back
    i = 0
    joined_cards = []
    for front in forged_cards_fronts:
        back = forged_cards_backs[i]
        i += 1
        if portrait:
            im = Image.new("RGBA", (front.width * 2, front.height))
            im.paste(front, box=(0, 0))
            im.paste(back, box=(front.width, 0))
            joined_cards.append(im)
        else:
            im = Image.new("RGBA", (front.width, front.height * 2))
            back = back.transpose(Image.ROTATE_180)
            im.paste(back, box=(0, 0))
            im.paste(front, box=(0, front.height))
            joined_cards.append(im)

    return weld_cards_standard(export, joined_cards, [])


def weld_cards_standard(export, forged_cards_fronts, forged_cards_backs):
    images_front, max_items_by_row = _weld_cards(export, forged_cards_fronts)

    if forged_cards_backs:
        # Reverse back order in groups of max_items_by_row
        forged_cards_backs_reordered = []
        empty_image = Image.new("RGBA", (forged_cards_fronts[0].width, forged_cards_fronts[0].height))

        while forged_cards_backs:
            chunk = forged_cards_backs[0:max_items_by_row]
            chunk += [empty_image] * (max_items_by_row - len(chunk))
            forged_cards_backs_reordered += reversed(chunk)
            forged_cards_backs = forged_cards_backs[max_items_by_row:]

        images_back, max_items_by_row = _weld_cards(export, forged_cards_backs_reordered)
        return [response for ab in zip(images_front, images_back) for response in ab]
    else:
        return images_front


def _weld_cards(export, forged_cards):
    images = []
    forged_cards_cut_marks = [add_cut_marks(card) for card in forged_cards]

    original_card = forged_cards[0]

    # Distribute uniformly
    if export['WIDTH'] != 0:
        page_width = export['WIDTH']
        page_height = export['HEIGHT']
        # Check without portrait
        portrait = False
        margin_x, margin_y, max_items_by_row, max_items_by_column = calculate_margins(export, original_card)
        card_portrait = original_card.transpose(Image.ROTATE_270)

        margin_x_portrait, margin_y_portrait, max_items_by_row_portrait, max_items_by_column_portrait = calculate_margins(
            export, card_portrait)
        if (max_items_by_row * max_items_by_column) < (max_items_by_row_portrait * max_items_by_column_portrait):
            margin_x = margin_x_portrait
            margin_y = margin_y_portrait
            max_items_by_row = max_items_by_row_portrait
            max_items_by_column = max_items_by_column_portrait
            original_card = card_portrait
            portrait = True

    else:
        max_items_by_row = 1
        max_items_by_column = 1
        margin_x = GROW
        margin_y = GROW
        page_width = forged_cards_cut_marks[0].width
        page_height = forged_cards_cut_marks[0].height
        portrait = False

    row = 0
    column = 0
    x = margin_x - GROW
    y = margin_y - GROW
    im = Image.new("RGBA", (page_width, page_height))

    for card in forged_cards_cut_marks:
        if card:
            if portrait:
                card = card.transpose(Image.ROTATE_270)

            im.paste(card, box=(x, y))
        x += margin_x + original_card.width
        row += 1
        if row == max_items_by_row:
            x = margin_x - GROW
            y += margin_y + original_card.height
            row = 0
            column += 1
            if column == max_items_by_column:
                _add_image_to_image_list(im, images)
                column = 0
                y = margin_y - GROW
                im = Image.new("RGBA", (page_width, page_height))

    if images == [] or images[-1] != im:
        if column != 0 or row != 0:
            _add_image_to_image_list(im, images)

    return images, max_items_by_row


def _add_image_to_image_list(image, image_list):
    rgb = Image.new('RGB', image.size, (255, 255, 255))  # white background
    rgb.paste(image, mask=image.split()[3])  # paste using alpha channel as mask
    image_list.append(rgb)
