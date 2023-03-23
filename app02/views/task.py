import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app02.models import Task
from app02.forms import TaskModelForm
from app02.utils import pagination


def task_list(request):
    """ 任务列表 """
    query_set = Task.objects.all().order_by('-id')

    form = TaskModelForm()

    page_obj = pagination.Pagination(request, query_set)
    page_query_set = page_obj.page_query_set
    page_list = page_obj.show_html()
    # return render(request, 'xxx.html', {'page_query_set': page_query_set, 'page_list': page_list})
    return render(request, 'task_list.html', {'form': form, 'task_data': page_query_set, 'page_list': page_list})


@csrf_exempt
def task_add(request):
    """ 给员工分配任务 """
    # 数据校验 前端传回的数据：request.POST
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        # request.session['info']['id'] 获取当前管理员（su）的id
        form.instance.leader_id = request.session['info']['id']
        form.save()
        data_dct = {'status': True}
        return HttpResponse(json.dumps(data_dct))
    data_dct = {'status': False, 'error': form.errors}
    # return HttpResponse(json.dumps(data_dct, ensure_ascii=False))
    return JsonResponse(data_dct)


def task_del(request, tid):
    """ 撤销任务 """
    # 取得待删除的任务id 即：tid
    exists = Task.objects.filter(id=tid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '该任务已被撤销或不存在'})
    # 若存在 则删除
    Task.objects.filter(id=tid).delete()
    return JsonResponse({'status': True})


@csrf_exempt
def task_edit(request, tid):
    """ 修改任务 """
    row_obj = Task.objects.filter(id=tid).first()
    if not row_obj:
        return JsonResponse({'status': False, 'error': '该任务已被撤销或不存在，请刷新后重试'})
    # GET
    if request.method == 'GET':
        row_data = Task.objects.filter(id=tid).values('title', 'level', 'user', 'project', 'detail').first()
        # result = {
        #     'status': True,
        #     'data': {
        #         'title': row_obj.title,
        #         'level': row_obj.level,
        #         'user': row_obj.user.user,
        #         'project': row_obj.project.name,
        #         'detail': row_obj.detail,
        #     }
        # }
        # print(result)  # JSON不支持序列化python对象，所以用 models.Model.objects.filter(...).values(...).first() 方法
        return JsonResponse({'status': True, 'data': row_data})
    # POST
    form = TaskModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        print('save')
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': '您提交了不合理的数据，请刷新后重试'})
