from PIL import Image, ImageDraw

size_troquel_mini = {
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
    'CUT_MARK_DISPLACEMENT': 35,
    'CUT_MARK_OVERLAP': 23,
    'CUT_MARK_SIZE': 37,
    'CUT_MARKS': True,
    'ROTATE': True
}

size_troquel_standard = {
    'NAME': 'standard',
    'WIDTH': 4960,
    'HEIGHT': 3507,
    'BOX_WIDTH': 811,
    'BOX_HEIGHT': 1106,
    'MARGIN_X': 113,
    'MARGIN_Y': 78,
    'GAP_X': 170,
    'GAP_Y': 17,
    'CARDS_PER_ROW': 5,
    'CUT_MARK_DISPLACEMENT': 33,
    'CUT_MARK_OVERLAP': 9,
    'CUT_MARK_SIZE': 62,
    'CUT_MARKS': True,
    'ROTATE': True
}

size_tabletop_mini = {
    'NAME': 'standard',
    'WIDTH': 5080,
    'HEIGHT': 5124,
    'BOX_WIDTH': 508,
    'BOX_HEIGHT': 732,
    'MARGIN_X': 0,
    'MARGIN_Y': 0,
    'GAP_X': 0,
    'GAP_Y': 0,
    'CARDS_PER_ROW': 10,
    'CUT_MARKS': False,
    'ROTATE': True
}


def create_image(size):
    im = Image.new("RGBA", (size['WIDTH'], size['HEIGHT']))

    paste_cards(size, im, [
        "../images/barracuda.png",
        "../images/barracuda.png",
        "../images/espada.png",
        "../images/espada.png",
        "../images/medusa.png",
        "../images/medusa.png",
        "../images/salazon.png",
        "../images/salazon.png",
        "../images/salazon.png",
        "../images/vendas.png",
        "../images/vendas.png",
        "../images/barril-agua.png",
        "../images/barril-agua.png",
        "../images/barril-agua.png",
        "../images/farol.png",
        "../images/farol.png",
        "../images/morena.png",
        "../images/morena.png",
        "../images/tesoro.png",
        "../images/tesoro.png",
        "../images/barril-rum.png",
        "../images/barril-rum.png",
        "../images/barril-rum.png",
        "../images/herramientas.png",
        "../images/pistola.png",
        "../images/tiburon.png",
        "../images/cana-pescar.png",
        "../images/cana-pescar.png",
        "../images/machete.png",
        "../images/machete.png",
        "../images/pulpo.png",
        "../images/pulpo.png",
        "../images/pulpo.png",
        "../images/tridente.png"
    ])
    im.save("copy.png")


def paste_cards(size, im, cards):
    x = size['MARGIN_X']
    y = size['MARGIN_Y']
    num = 0
    for card_file in cards:
        card = Image.open(card_file)
        if size['ROTATE']:
            card = card.transpose(Image.ROTATE_270)
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


if __name__ == "__main__":
    create_image(size_troquel_mini)
