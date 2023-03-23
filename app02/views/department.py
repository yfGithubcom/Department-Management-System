from django.shortcuts import render, redirect
from app02.models import Department
from app02.forms import DepartmentModelForm
from django.utils.safestring import mark_safe
from app02.utils import pagination


# Create your views here.

# department
def department_list(request):
    """部门列表"""
    # get data from mysql
    department_data = Department.objects.all()
    page_obj = pagination.Pagination(request, query_set=department_data)
    page_query_set = page_obj.page_query_set
    page_list = page_obj.show_html()
    return render(request, 'department_list.html', {'department_data': page_query_set, 'page_list': page_list})


def department_add(request):
    """添加部门"""
    if request.method == 'GET':
        form = DepartmentModelForm()
        return render(request, 'department_add.html', {'form': form})
    form = DepartmentModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/department/list/')
    return render(request, 'department_add.html', {'form': form})


def department_del(request):
    """删除部门"""
    dpt_id = request.GET.get('did')
    Department.objects.filter(id=dpt_id).delete()
    return redirect('/department/list/')


def department_edit(request, did):
    """修改部门"""
    row_obj = Department.objects.filter(id=did).first()
    if request.method == 'GET':
        form = DepartmentModelForm(instance=row_obj)
        return render(request, 'department_edit.html', {'form': form, 'did': did})
    form = DepartmentModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        # return redirect(f'/department/{did}/edit/')
        return redirect('/department/list/')
    return render(request, 'department_edit.html', {'form': form, 'did': did})
