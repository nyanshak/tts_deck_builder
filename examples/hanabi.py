import os

from PIL import Image, ImageFont

from tts_deck_builder import (
    generate_background,
    hex2rgb,
    get_card,
    get_card_with_logo,
    paste_image_center,
    draw_centered_text
)


def main():
    card_width = 408
    card_height = 585

    main_deck_font = 'assets/fonts/Go-Bold.ttf'
    hint_deck_font = 'assets/fonts/Go-Bold.ttf'

    main_deck_font_size = 124
    hint_deck_font_size = 124

    main_card_back_color = hex2rgb("#091E42")

    hint_card_front_color = hex2rgb("#FFFFFF")
    hint_card_back_color = hex2rgb("#091E42")
    hint_card_font_color = hex2rgb("#091E42")

    main_card_back_logo = "assets/icons/heart-white.png"
    hint_card_back_logo = "assets/icons/heart-white.png"

    output_dir = "output/hanabi"

    suits = [
        {
            "name": "yellow",
            "font_color": hex2rgb("#EBB038"),
            "background_color": hex2rgb("#FAFBFC"),
            "icon_file": "assets/icons/heart-yellow.png",
            "logo_file": "assets/icons/heart-black.png"
        },
        {
            "name": "red",
            "font_color": hex2rgb("#CB5436"),
            "background_color": hex2rgb("#FAFBFC"),
            "icon_file": "assets/icons/heart-red.png",
            "logo_file": "assets/icons/heart-black.png"
        },
        {
            "name": "blue",
            "font_color": hex2rgb("#4C9AFF"),
            "background_color": hex2rgb("#FAFBFC"),
            "icon_file": "assets/icons/heart-blue.png",
            "logo_file": "assets/icons/heart-black.png"
        },
        {
            "name": "green",
            "font_color": hex2rgb("#57AF89"),
            "background_color": hex2rgb("#FAFBFC"),
            "icon_file": "assets/icons/heart-green.png",
            "logo_file": "assets/icons/heart-black.png"
        },
        {
            "name": "purple",
            "font_color": hex2rgb("#B1A7EC"),
            "background_color": hex2rgb("#FAFBFC"),
            "icon_file": "assets/icons/heart-purple.png",
            "logo_file": "assets/icons/heart-black.png"
        }
    ]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    font = ImageFont.truetype(
        main_deck_font, size=main_deck_font_size)

    for suit in suits:
        card_bg = generate_background(
            card_width, card_height, suit["background_color"])
        card_bg = get_card_with_logo(
            card_bg, suit["logo_file"], logo_scale_factor=0.475)
        for i in range(1, 6):
            output_file = f"{output_dir}/{suit['name']}-{i}.jpg"

            card_text = f"{i}"
            card = get_card(
                card_bg, suit['icon_file'], font,
                card_text, i, font_color=suit['font_color'])

            card.save(output_file, quality=95)

    back_card = generate_background(
        card_width, card_height, main_card_back_color)
    logo = Image.open(main_card_back_logo)
    back_card = paste_image_center(back_card, logo, scale_factor=0.7)
    back_card.save(f"{output_dir}/back.jpg")

    # Generate hint number cards
    hint_font = ImageFont.truetype(
        hint_deck_font, size=hint_deck_font_size)
    hint_card_size = int(0.5 * float(card_width))
    for i in range(1, 6):
        hint_card = generate_background(
            hint_card_size, hint_card_size, hint_card_front_color)

        hint_card = draw_centered_text(
            hint_card, f"{i}", hint_font, hint_card_font_color)
        hint_card.save(f"{output_dir}/hint-{i}.jpg")

    for suit in suits:
        hint_card_base = generate_background(
            hint_card_size, hint_card_size, hint_card_front_color)
        logo = Image.open(suit['icon_file'])
        hint_card = paste_image_center(hint_card_base, logo, scale_factor=0.7)
        hint_card.save(f"{output_dir}/hint-{suit['name']}.jpg")

    # generate hint back
    logo = Image.open(hint_card_back_logo)
    hint_card_base = generate_background(
        hint_card_size, hint_card_size, hint_card_back_color)
    hint_back = paste_image_center(hint_card_base, logo, scale_factor=0.7)
    hint_back.save(f"{output_dir}/hint-back.jpg")


if __name__ == '__main__':
    main()
