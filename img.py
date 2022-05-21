from typing import KeysView
from pilmoji import Pilmoji
import io
import requests
import datetime
import textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from PIL import Image, ImageFont
import re


def time():
    dt_now = datetime.datetime.now()
    return dt_now.strftime("%m月%d日-%H時%M分")


def textimg(text):
    dict = {}
    for i in re.findall("<.?:[^>]*:[0-9]{18}>", text):
        dict[text.find(i)] = i
        text = text.replace(i, "")
    if len(str(text)) > 72:
        text = text[0:69] + "．．．"
        im = Image.new("RGBA", (1500, 400), (0, 0, 0))
        im.putalpha(0)
        pilmoji = Pilmoji(im)
        wrap_list = "\n".join(textwrap.wrap(text, 18))
        list_wrap = list(wrap_list)
        for dict_key, dict_value in dict.items():
            wrap_list.insert(dict_key, dict_value)
        wrap_list = "".join(list_wrap)
        font = ImageFont.truetype("font_text/BIZ-UDGOTHICR.TTC", 80)
        pilmoji.text((45, 50), wrap_list.strip(), fill=(255, 255, 255), font=font)
        img_bytes = io.BytesIO()
        im.save(img_bytes, format="png")
        return img_bytes
    else:
        im = Image.new("RGBA", (1500, 400), (0, 0, 0))
        im.putalpha(0)
        pilmoji = Pilmoji(im)
        wrap_list = "\n".join(textwrap.wrap(text, 18))
        list_wrap = list(wrap_list)
        for dict_key, dict_value in dict.items():
            list_wrap.insert(dict_key, dict_value)
        wrap_list = "".join(list_wrap)
        font = ImageFont.truetype("font_text/BIZ-UDGOTHICR.TTC", 80)
        pilmoji.text((45, 50), wrap_list.strip(), fill=(255, 255, 255), font=font)
        img_bytes = io.BytesIO()
        im.save(img_bytes, format="png")
        return img_bytes


def name_time(img, username, time):
    font = ImageFont.truetype("font_text/BIZ-UDGOTHICR.TTC", 80)
    with Pilmoji(img) as pilmoji:
        pilmoji.text((50, 40), username, (255, 255, 255), font=font)
        pilmoji.text((1250, 40), time(), (255, 255, 255), font=font)
        image_bytes = io.BytesIO()
        pilmoji.save(image_bytes, format="png")
        image_bytes.seek(0)
        return pilmoji


def image_cut(icon_url):
    offset = 2
    gif = io.BytesIO(requests.get(icon_url).content)
    img = Image.open(gif).convert("RGB")
    mask = Image.new("L", img.size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse([(offset, offset), (img.size[0] - offset, img.size[1] - offset)], 255)
    del draw
    img.putalpha(mask)
    img = img.resize((400, 400))
    image_bytes = io.BytesIO()
    img.save(image_bytes, format="png")
    return image_bytes


def make_image(icon_url, text, username):
    font = ImageFont.truetype("font_text/BIZ-UDGOTHICR.TTC", 80)
    base = Image.open("base_image/base0.jpg")
    icon = Image.open((image_cut(icon_url))).convert("RGBA")
    text = Image.open(textimg(text))
    base.paste(icon, (50, 190), icon)
    base.paste(text, (450, 150), text)
    with Pilmoji(base) as pilmoji:
        pilmoji.text((50, 40), username.strip(), (255, 255, 255), font=font)
        pilmoji.text((1250, 40), time().strip(), (255, 255, 255), font=font)
        image_bytes = io.BytesIO()
        base.save(image_bytes, format="png")
        image_bytes.seek(0)
        return image_bytes
