from io import BytesIO

from django.shortcuts import render, redirect
from django.http import HttpResponse

from app02.forms import LoginForm
from app02.models import Su
from app02.utils import captcha


def login(request):
    """管理员的登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 没有创建相关models，此处不进行form.save()
        dct = form.cleaned_data  # 如：{'su': '123321', 'password': '123456'} 为字典格式

        input_code = dct.pop('img_code')  # 去掉验证码键值对，验证码不存入数据库，返回用户输入的验证码
        captcha_code = request.session.get('img_code', '')  # 获取系统生成的验证码，若未查到，返回空
        if input_code != captcha_code:
            form.add_error('img_code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        su_obj = Su.objects.filter(**dct).first()
        if not su_obj:  # 管理员的用户名或密码错误
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确，网站生成随机字符串作为用户浏览器的cookie，写入session中
        request.session['info'] = {'id': su_obj.id, 'su': su_obj.su}
        request.session.set_expiry(60 * 60 * 24 * 7)  # 7天失效
        return redirect('/')
    return render(request, 'login.html', {'form': form})


def img_code(request):
    """访问时生成验证码图片"""
    img, captcha_text = captcha.generate_captcha()
    # 将验证码字符串写入 session 中，便于后续校验
    request.session['img_code'] = captcha_text
    # 设置验证码超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """管理员账号登出"""
    request.session.clear()
    return redirect('/')
