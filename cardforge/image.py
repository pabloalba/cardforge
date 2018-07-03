from PIL import Image, ImageDraw

size_mini = {
    'NAME': 'mini',
    'WIDTH': 4960,
    'HEIGHT': 3507,
    'BOX_WIDTH': 597,
    'BOX_HEIGHT': 822,
    'MARGIN_X': 73,
    'MARGIN_Y': 73,
    'GAP_X': 106,
    'GAP_Y': 25,
    'CARDS_PER_ROW': 7,
    'CUT_MARK_X': 35,
    'CUT_MARK_Y': 23,
    'CUT_MARK_SIZE': 37
}

size_standard = {
    'NAME': 'standard',
    'WIDTH': 4960,
    'HEIGHT': 3507,
    'BOX_WIDTH': 811,
    'BOX_HEIGHT': 1106,
    'MARGIN_X': 113,
    'MARGIN_Y': 78,
    'GAP_X': 170,
    'GAP_Y': 17,
    'CARDS_PER_ROW': 5
}


def create_image(size):
    im = Image.open("base_{}.png".format(size['NAME']))
    im.mode = "RGBA"

    paste_cards(size, im, ["lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png",
                           "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png",
                           "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png",
                           "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png", "lanza.png"
                           ])
    set_cut_marks(size, im)

    im.save("copy.png")


def set_cut_marks(size, im):
    marcas = Image.open("marcas_corte_cartas_{}.png".format(size['NAME']))
    im.paste(marcas, box=None, mask=marcas)


def paste_cards(size, im, cards):
    x = size['MARGIN_X']
    y = size['MARGIN_Y']
    num = 0
    for card_file in cards:
        card = Image.open(card_file)
        card = card.transpose(Image.ROTATE_90)
        paste_card(size, im, card, x, y)
        x += size['GAP_X'] + size['BOX_WIDTH']
        num += 1
        if num == size['CARDS_PER_ROW']:
            x = size['MARGIN_X']
            y += size['GAP_Y'] + size['BOX_HEIGHT']
            num = 0


def paste_card(size, im, card, x, y):
    # draw margin
    box = (x, y, x + size['BOX_WIDTH'], y + size['BOX_HEIGHT'])
    im.paste("black", box=box)

    # draw card
    margin_x = int(round((size['BOX_WIDTH'] - card.width) / 2))
    margin_y = int(round((size['BOX_HEIGHT'] - card.height) / 2))
    box = (x + margin_x, y + margin_y)
    print(box)
    im.paste(card, box=box)

    # draw cut marks
    draw = ImageDraw.Draw(im)
    pos_x = x+size['CUT_MARK_X']
    pos_y = y+size['CUT_MARK_Y']

    draw.line((pos_x, pos_y, pos_x, pos_y - size['CUT_MARK_SIZE']), fill=(0,255,0,255))
    draw.line((pos_x + 1, pos_y, pos_x + 1, pos_y - size['CUT_MARK_SIZE']), fill=(0,255,0,255))

    pos_x = x + size['BOX_WIDTH'] - size['CUT_MARK_X'] - 2
    pos_y = y+size['CUT_MARK_Y']

    draw.line((pos_x, pos_y, pos_x, pos_y - size['CUT_MARK_SIZE']), fill=(0,255,0,255))
    draw.line((pos_x + 1, pos_y, pos_x + 1, pos_y - size['CUT_MARK_SIZE']), fill=(0,255,0,255))




    del draw



if __name__ == "__main__":
    create_image(size_mini)
