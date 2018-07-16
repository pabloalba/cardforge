import uuid

from PIL import Image, ImageDraw

from .sizes import size_troquel_mini


def forge_deck(deck):
    forged_cards = forge_cards(deck)
    size = size_troquel_mini

    images = weld_cards(size, forged_cards)

    file_path_pdf = "/tmp/{}.pdf".format(uuid.uuid4())

    # Convert images to
    images[0].save(file_path_pdf, save_all=True, append_images=images[1:], resoultion=300.0)

    return file_path_pdf


def forge_cards(deck):
    return [
        "/tmp/naufragio/barracuda.png",
        "/tmp/naufragio/barracuda.png",
        "/tmp/naufragio/espada.png",
        "/tmp/naufragio/espada.png",
        "/tmp/naufragio/medusa.png",
        "/tmp/naufragio/medusa.png",
        "/tmp/naufragio/salazon.png",
        "/tmp/naufragio/salazon.png",
        "/tmp/naufragio/salazon.png",
        "/tmp/naufragio/vendas.png",
        "/tmp/naufragio/vendas.png",
        "/tmp/naufragio/barril-agua.png",
        "/tmp/naufragio/barril-agua.png",
        "/tmp/naufragio/barril-agua.png",
        "/tmp/naufragio/farol.png",
        "/tmp/naufragio/farol.png",
        "/tmp/naufragio/morena.png",
        "/tmp/naufragio/morena.png",
        "/tmp/naufragio/tesoro.png",
        "/tmp/naufragio/tesoro.png",
        "/tmp/naufragio/barril-rum.png",
        "/tmp/naufragio/barril-rum.png",
        "/tmp/naufragio/barril-rum.png",
        "/tmp/naufragio/herramientas.png",
        "/tmp/naufragio/pistola.png",
        "/tmp/naufragio/tiburon.png",
        "/tmp/naufragio/cana-pescar.png",
        "/tmp/naufragio/cana-pescar.png",
        "/tmp/naufragio/machete.png",
        "/tmp/naufragio/machete.png",
        "/tmp/naufragio/pulpo.png",
        "/tmp/naufragio/pulpo.png",
        "/tmp/naufragio/pulpo.png",
        "/tmp/naufragio/tridente.png"
    ]


def weld_cards(size, cards):
    images = []
    x = size['MARGIN_X']
    y = size['MARGIN_Y']
    num = 0
    rows = 0
    im = Image.new("RGBA", (size['WIDTH'], size['HEIGHT']))
    for card_file in cards:
        card = Image.open(card_file)
        if size['ROTATE']:
            card = card.transpose(Image.ROTATE_270)
        weld_card(size, im, card, x, y)
        x += size['GAP_X'] + size['BOX_WIDTH']
        num += 1
        if num == size['CARDS_PER_ROW']:
            x = size['MARGIN_X']
            y += size['GAP_Y'] + size['BOX_HEIGHT']
            num = 0
            rows += 1
            if rows == size['ROWS']:
                _add_image_to_image_list(im, images)
                im = Image.new("RGBA", (size['WIDTH'], size['HEIGHT']))
                rows = 0
                x = size['MARGIN_X']
                y = size['MARGIN_Y']

    if images == [] or images[-1] != im:
        _add_image_to_image_list(im, images)

    return images


def _add_image_to_image_list(image, image_list):
    rgb = Image.new('RGB', image.size, (255, 255, 255))  # white background
    rgb.paste(image, mask=image.split()[3])  # paste using alpha channel as mask
    image_list.append(rgb)


def weld_card(size, im, card, x, y):
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
