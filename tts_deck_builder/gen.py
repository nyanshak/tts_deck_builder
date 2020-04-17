from PIL import Image, ImageDraw


def generate_background(width, height, color=(255, 255, 255)):
    image = Image.new('RGB', (width, height), color)
    return image


def rotate_image(image, degrees=180):
    return image.rotate(degrees, resample=Image.BICUBIC, expand=True)


# Generate a mask with text
def get_font_image(font, text):
    font_width, font_height = font.getsize(text)

    font_image = Image.new('L', (font_width, font_height))

    ImageDraw.Draw(font_image).text(
        (0, 0),
        text,
        fill=255,
        font=font
    )
    return font_image


# get_box determines where to overlay an image on another.
#
# if mirror is True, generates offset from bottom right corner instead
def get_box(bg_image, paste_image, horizontal_pad, vertical_pad, mirror=False):
    left = horizontal_pad
    upper = vertical_pad
    right = horizontal_pad + paste_image.width
    lower = vertical_pad + paste_image.height

    if mirror:
        left = bg_image.width - (horizontal_pad + paste_image.width)
        upper = bg_image.height - (vertical_pad + paste_image.height)
        right = bg_image.width - horizontal_pad
        lower = bg_image.height - vertical_pad
    return (left, upper, right, lower)


def get_card_with_text_value(card_image, font_image, font_color, hpad, vpad):
    out_image = card_image.copy()

    rotated_font_image = rotate_image(font_image)

    normal_box = get_box(out_image, font_image, hpad, vpad)
    rotated_box = get_box(out_image, font_image, hpad, vpad, mirror=True)

    out_image.paste(font_color, box=normal_box, mask=font_image)
    out_image.paste(font_color, box=rotated_box, mask=rotated_font_image)

    return out_image


def get_card_with_suit_image(card_image, suit_image, hpad, vpad):
    out_image = card_image.copy()

    rotated_image = rotate_image(suit_image)

    normal_box = get_box(out_image, suit_image, hpad, vpad)
    rotated_box = get_box(out_image, suit_image, hpad, vpad, mirror=True)

    out_image.paste(suit_image, box=normal_box, mask=suit_image)
    out_image.paste(rotated_image, box=rotated_box, mask=rotated_image)

    return out_image


# Resizes image to have proportional size to base_image
def resize_image(base_image, image, scale_factor=1.0, by_width=True):
    if by_width:
        new_width = int(float(base_image.width) * scale_factor)
        width_percent = (new_width / float(image.width))
        new_height = int(float(image.height) * float(width_percent))
    else:
        new_height = int(float(base_image.height) * scale_factor)
        height_percent = (new_height / float(image.height))
        new_width = int(float(image.width) * float(height_percent))

    bands = image.split()
    bands = [b.resize((new_width, new_height), Image.ANTIALIAS) for b in bands]
    return Image.merge('RGBA', bands)


# bg_image and suit_icon are PIL.Image
def get_card(bg_image, suit_icon, font, card_text,
             value, font_color=(5, 200, 13)):
    card_image = bg_image.copy()

    font_width, font_height = font.getsize(card_text)

    hpad = 35
    base_vpad = 15
    sep_vpad = 10

    font_image = get_font_image(font, card_text)

    card_image = get_card_with_text_value(
        card_image, font_image, font_color, hpad, base_vpad
    )

    suit_image = Image.open(suit_icon).convert("RGBA").copy()
    suit_image = resize_image(
        font_image, suit_image, by_width=False, scale_factor=0.6)

    center = float(hpad) + (0.5 * float(font_image.width))
    hpad = int(center - 0.5 * float(suit_image.width))
    for i in range(value):
        vpad = base_vpad + font_image.height + \
                (sep_vpad * (i + 1)) + \
                (suit_image.height * i)

        card_image = get_card_with_suit_image(
            card_image, suit_image, hpad, vpad)

    return card_image


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hex2rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))


def get_card_with_logo(card_bg, logo_file, logo_scale_factor=0.475):
    card_bg = card_bg.copy()

    logo = Image.open(logo_file)
    logo = resize_image(card_bg, logo, scale_factor=logo_scale_factor)

    left = int(0.5 * float(card_bg.width - logo.width))
    upper = int(0.5 * float(card_bg.height - logo.height))

    card_bg.paste(logo, box=(left, upper), mask=logo)

    return card_bg


def paste_image_center(bg_image, paste_image, scale_factor=1.0):
    bg_image = bg_image.copy()
    paste_image = paste_image.copy()

    paste_image = resize_image(
        bg_image, paste_image, scale_factor=scale_factor)

    left = int(0.5 * float(bg_image.width - paste_image.width))
    upper = int(0.5 * float(bg_image.height - paste_image.height))

    bg_image.paste(paste_image, box=(left, upper), mask=paste_image)
    return bg_image


def draw_centered_text(bg_image, message, font, color):
    bg_image = bg_image.copy()

    draw = ImageDraw.Draw(bg_image)
    w, h = draw.textsize(message, font)

    position = (
        (bg_image.width - w) / 2,
        (bg_image.height - h) / 2
    )

    draw.text(position, message, color, font=font)
    return bg_image
