"""
在跳转前检查登录状态

检查用户是否已经登录，若未登录，跳转至登录界面
用户发送请求，获取 cookie 字符串，将 cookie 与数据库中的 session 进行比对
"""
from django.shortcuts import redirect


def check_login(request):
    info = request.session.get('info')  # 已登录 {'id': 2, 'su': 'test2'} ，未登录 None
    if not info:  # 没有保存登录信息，cookie为None
        return redirect('/login/')
