import random
import string
# Image：畫布
# ImageDraw：畫筆
# ImageFont:字體
from PIL import Image, ImageDraw, ImageFont

from flask import current_app
import os


# pip install pillow

# Captcha驗證碼


class Captcha(object):
    # 生成驗證碼位數
    number = 4
    # 驗證碼圖片的寬高
    size = (100, 30)
    # 驗證碼字體大小
    fontsize = 25
    # 干擾線條數
    line_number = 2

    # 創建一個驗證碼字串
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 繪製干擾線
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    # 繪製干擾點
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    # 生成隨機顏色
    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        random.seed()
        # 隨機生成RGB 0-255 各一個顏色
        return (random.randint(start, end), random.randint(start, end), random.randint(start, end))

    # 隨機選擇字體
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            'Courgette-Regular.ttf',
            'LHANDW.TTF',
            'Lobster-Regular.ttf',
            'verdana.ttf'
        ]
        font = random.choice(fonts)
        fontpath = os.path.join(current_app.config['BASE_DIR'], 'utils', 'captcha', font)
        # return 'utils/captcha/'+font
        return fontpath

    # 用来隨機生成字串
    @classmethod
    def gene_text(cls, number):
        # number是生成驗證碼位數
        return ''.join(random.sample(cls.SOURCE, number))

    # 生成驗證碼
    @classmethod
    def gene_graph_captcha(cls):
        # 驗證碼圖片大小
        width, height = cls.size
        # 繪製圖片
        # R：Red 0-255
        # G：G 0-255
        # B：B 0-255
        # A：Alpha（透明度）
        image = Image.new('RGBA', (width, height), cls.__gene_random_color(0, 100))
        # 驗證碼字體
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        # 畫筆
        draw = ImageDraw.Draw(image)
        # 生成字串
        text = cls.gene_text(cls.number)
        # 獲得字體大小
        font_width, font_height = font.getsize(text)
        # 填入字串並置中
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font,
                  fill=cls.__gene_random_color(150, 255))
        # 繪製干擾線
        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
        # 繪製噪點
        cls.__gene_points(draw, 10, width, height)
        return (text, image)
