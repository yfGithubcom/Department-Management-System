# from PIL import Image, ImageDraw, ImageFont
#
# img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
# draw = ImageDraw.Draw(img, mode='RGB')
#
# font = ImageFont.truetype('Monaco.ttf', 28)
# context = 'hello'
# draw.text([0, 0], context, 'red', font)
#
# with open('code.png', 'wb') as f:
#     img.save(f, format='png')

"""captcha"""

from random import randint
from PIL import Image, ImageDraw, ImageFont


def generate_captcha(size=(180, 50),
                     chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                     font_size=30,
                     noise_points=100,
                     noise_lines=5):
    """
    生成随机字符验证码图片
    :param size: 验证码图片大小
    :param chars: 随机字符集合，默认为字母和数字
    :param font_size: 验证码字体大小
    :param noise_points: 噪点数量
    :param noise_lines: 干扰线数量
    :return: 生成的验证码图片
    """
    # 创建Image对象，设置背景色为白色
    img = Image.new('RGB', size, 'white')

    # 获取ImageDraw对象
    draw = ImageDraw.Draw(img)

    # 创建字体对象
    font = ImageFont.truetype('arial.ttf', font_size)

    # 获取验证码字符
    captcha_text = ''.join([chars[randint(0, len(chars) - 1)] for i in range(4)])

    # 绘制验证码字符
    for i in range(4):
        draw.text((i * (size[0] / 4) + 10, 20), captcha_text[i], font=font, fill=(0, 0, 0))

    # 绘制噪点
    for i in range(noise_points):
        x = randint(0, size[0] - 1)
        y = randint(0, size[1] - 1)
        draw.point((x, y), fill=(0, 0, 0))

    # 绘制干扰线
    for i in range(noise_lines):
        x1 = randint(0, size[0] - 1)
        y1 = randint(0, size[1] - 1)
        x2 = randint(0, size[0] - 1)
        y2 = randint(0, size[1] - 1)
        draw.line((x1, y1, x2, y2), fill=(0, 0, 0))

    return img, captcha_text


if __name__ == '__main__':
    with open('code.png', 'wb') as f:
        img, captcha_text = generate_captcha()
        img.save(f, format('png'))
