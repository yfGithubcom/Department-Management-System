from django.shortcuts import render, redirect
from app02.models import Su
from app02.forms import SuModelForm, SuEditModelForm, SuResetModelForm
from django.utils.safestring import mark_safe
from app02.utils import pagination


# Create your views here.

# admin
def su_list(request):
    """管理员用户"""
    value = request.GET.get('search')
    dct = {}
    if value:  # 若触发查询
        dct['su__contains'] = value
    su_data = Su.objects.filter(**dct)
    page_obj = pagination.Pagination(request, query_set=su_data)
    page_query_set = page_obj.page_query_set
    page_list = page_obj.show_html()
    return render(request, 'su_list.html', {'su_data': page_query_set, 'page_list': page_list})


def su_add(request):
    """添加管理员"""
    if request.method == 'GET':
        form = SuModelForm
        return render(request, 'su_add.html', {'form': form})
    form = SuModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect('/su/list/')
    return render(request, 'su_add.html', {'form': form})


def su_edit(request, suid):
    """编辑管理员账号"""
    row_obj = Su.objects.filter(id=suid).first()
    if not row_obj:
        return render(request, 'error.html', {'msg': '数据不存在'})
    if request.method == 'GET':
        form = SuEditModelForm(instance=row_obj)
        return render(request, 'su_edit.html', {'form': form, 'suid': suid})
    form = SuEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/su/list/')
        # return redirect(f'/su/{suid}/edit/')
    return render(request, 'su_edit.html', {'form': form, 'suid': suid})


def su_del(request, suid):
    """删除管理员账号"""
    Su.objects.filter(id=suid).delete()
    return redirect('/su/list/')


def su_reset(request, suid):
    """管理员账号密码重置"""
    row_obj = Su.objects.filter(id=suid).first()
    if not row_obj:
        return redirect('/su/list/')

    if request.method == 'GET':
        form = SuResetModelForm()  # instance=row_obj 不展示密码
        return render(request, 'su_reset.html', {'form': form, 'suid': suid})

    form = SuResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/su/list/')
        # return redirect(f'/su/{suid}/reset/')
    return render(request, 'su_reset.html', {'form': form, 'suid': suid})
