from io import BytesIO
from captcha.image import ImageCaptcha
from PIL import Image
from random import choices
from fastapi.responses import StreamingResponse


# 第一步： 生成验证码
def gen_captcha(content='2345689abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ'):
    """ 生成验证码 """
    image = ImageCaptcha()
    # 获取字符串
    captcha_text = "".join(choices(content, k=4)).lower()
    # 生成图像
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image




# 第二步：返回验证码及格式，
def get_captcha():
    code, image = gen_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    # resp = make_response(out.read())
    # resp.content_type = 'image/png'
    resp = StreamingResponse(out, media_type="image/png")
    return resp, code




