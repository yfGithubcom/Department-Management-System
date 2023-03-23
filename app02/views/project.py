from django.shortcuts import render, redirect
from app02.models import Project
from app02.forms import ProjectModelForm
from django.utils.safestring import mark_safe
from app02.utils import pagination


# Create your views here.

# project
def project_list(request):
    """项目列表"""
    # project_data = Project.objects.all().order_by('level')

    value = request.GET.get('search')
    dct = {}
    if value:  # 若触发查询
        dct['name__contains'] = value
    project_data = Project.objects.filter(**dct)
    # 创建分页类
    page_obj = pagination.Pagination(request, query_set=project_data, plus=2)
    page_query_set = page_obj.page_query_set
    page_list = page_obj.show_html()
    return render(request, 'project_list.html', {'project_data': page_query_set, 'page_list': page_list})


def project_add(request):
    """新增项目"""
    if request.method == 'GET':
        form = ProjectModelForm()
        return render(request, 'project_add.html', {'form': form})
    form = ProjectModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/project/list/')
    return render(request, 'project_add.html', {'form': form})


def project_edit(request, p_id):
    """编辑项目"""
    row_obj = Project.objects.filter(id=p_id).first()
    if request.method == 'GET':
        form = ProjectModelForm(instance=row_obj)
        return render(request, 'project_edit.html', {'form': form, 'p_id': p_id})
    form = ProjectModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect(f'/project/{p_id}/edit/')
    return render(request, 'project_edit.html', {'form': form, 'p_id': p_id})


def project_del(request, p_id):
    """删除项目"""
    Project.objects.filter(id=p_id).delete()
    return redirect('/project/list/')
