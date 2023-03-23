from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.http import HttpResponse


# 如果方法中有返回值，比如 HttpResponse、render、redirect等，则随即返回用户，不再继续向后执行

class AuthMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        # 排除不需要登录也可以访问的页面  request.path_info 获取当前用户请求的url
        request_without_login_list = [
            '/login/',
            '/img/code/',
            # '/index/',
        ]
        if request.path_info in request_without_login_list:
            return None
        # 读取当前访问用户的session信息，如果存在，则代表用户曾经登录过
        info = request.session.get('info')
        # 已登录过
        if info:
            return None
        # 未登录
        return redirect('/login/')
