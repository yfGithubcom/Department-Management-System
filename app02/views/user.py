from django.shortcuts import render, redirect
from app02.models import User
from app02.forms import UserModelForm
from django.utils.safestring import mark_safe
from app02.utils import pagination


# Create your views here.

# user
def user_list(request):
    """用户列表"""
    # 查询
    value = request.GET.get('search')  # 获取搜索框内的值
    dct = {}
    if value:  # 若触发查询
        dct['user__contains'] = value
    user_data = User.objects.filter(**dct)
    # 创建分页类
    page_obj = pagination.Pagination(request, query_set=user_data)
    page_query_set = page_obj.page_query_set
    page_list = page_obj.show_html()
    return render(request, 'user_list.html', {'user_data': page_query_set, 'page_list': page_list})


# ---- ModelForm示例 ----
def user_add(request):
    """用户添加（ModelForm）"""
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {'form': form})
    # 用户使用POST提交数据
    form = UserModelForm(data=request.POST)
    # 进行数据校验
    if form.is_valid():
        # print(form.cleaned_data)  # 数据合法
        form.save()
        return redirect('/user/list/')
    # 校验失败
    # print(form.errors)  # 数据不合法，在页面上显示错误信息
    return render(request, 'user_model_form_add.html', {'form': form})


def user_edit(request, uid):
    """编辑用户"""
    row_obj = User.objects.filter(id=uid).first()
    if request.method == 'GET':
        # 根据 uid（user_id） 获取数据
        form = UserModelForm(instance=row_obj)  # instance
        return render(request, 'user_edit.html', {'form': form, 'uid': uid})
    # post 提交表单
    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():  # 校验合法
        # 默认只保存用户输入的所有数据，若想在此基础上给字段设置默认值 form.instance.your_field = your_value
        form.save()  # 保存数据
        # return redirect('/user/list/')  # 修改成功后，返回用户展示列表
        return redirect(f'/user/{uid}/edit/')  # 修改成功后，留在修改界面，不返回用户展示列表
    return render(request, 'user_edit.html', {'form': form, 'uid': uid})  # 数据不合法，重定向回修改页，继续输入修改数据


def user_del(request, uid):
    """删除用户"""
    User.objects.filter(id=uid).delete()
    # user_data = User.objects.all()  # way1
    # return render(request, 'user_list.html', {'user_data': user_data})
    return redirect('/user/list/')  # way2
