from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

import datetime
import pendulum

from app02.models import Department, User, Project


def chart_list(request):
    """ 数据统计页面 """
    return render(request, 'chart_list.html')


def chart_bar(request):
    """ department_bar """
    dpt_data = Department.objects.all()
    dpt_id_lst = [dpt.id for dpt in dpt_data]
    dpt_lst = [dpt.unit for dpt in dpt_data]  # ['运维部门', '人力资源部门', '策划部门', '财务部门', '测试部门', '企划部']
    user_male_data = [User.objects.filter(gender=1).filter(unit=unit_id).count() for unit_id in dpt_id_lst]
    user_female_data = [User.objects.filter(gender=2).filter(unit=unit_id).count() for unit_id in dpt_id_lst]

    bar_title_text = '各部门人数'
    bar_legend_data = ['男', '女']  # 性别
    bar_xAxis_data = dpt_lst  # 部门列表
    bar_series = [
        {
            'name': '男',
            'type': 'bar',
            'data': user_male_data,
        },
        {
            'name': '女',
            'type': 'bar',
            'data': user_female_data,
        }
    ]

    res = {
        'status': True,
        'data': {
            'bar_title_text': bar_title_text,
            'bar_legend_data': bar_legend_data,
            'xAxis_data': bar_xAxis_data,
            'bar_series': bar_series,
        }
    }
    return JsonResponse(res)


def chart_pie(request):
    """ project_pie """
    # (1, '未启动'), (2, '进行中'), (3, '待交付'), (4, '已结束')
    status_dct = {
        1: '未启动',
        2: '进行中',
        3: '待交付',
        4: '已结束'
    }
    data_dct = {}
    for i in range(1, 5):
        total = Project.objects.filter(status=i).count()
        data_dct[status_dct[i]] = total
    # 排序
    sorted_dct = sorted(data_dct.items(),
                        key=lambda n: n[1],
                        reverse=True)  # [('待交付', 11), ('已结束', 10), ('未启动', 8), ('进行中', 4)]

    pie_title_text = '项目完成情况'
    pie_series_data = [{'value': v, 'name': k} for k, v in sorted_dct]
    # pie_series_data = [
    #     {'value': 1048, 'name': 'Search Engine'},
    #     {'value': 735, 'name': 'Direct'},
    #     {'value': 580, 'name': 'Email'},
    #     {'value': 484, 'name': 'Union Ads'},
    #     {'value': 300, 'name': 'Video Ads'}
    # ]

    res = {
        'status': True,
        'data': {
            'pie_title_text': pie_title_text,
            'pie_series_data': pie_series_data,
        }
    }
    return JsonResponse(res)


def chart_line(request):
    """ entry_line """

    def get_date_list(days):
        """返回前days天日期列表"""
        date_lst = []

        for i in range(1, days + 1):
            day = datetime.datetime.now() - datetime.timedelta(days=i)
            one_date = datetime.datetime(day.year, day.month, day.day).strftime('%Y-%m-%d')
            date_lst.append(one_date)

        return date_lst

    date_lst = get_date_list(7)
    week_list = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    line_title_text = '一周内入职员工'
    line_xAxis_data = [week_list[pendulum.parse(i).day_of_week] for i in date_lst][::-1]
    # print(line_xAxis_data)
    line_series_data = [User.objects.filter(entry_date=i).count() for i in date_lst][::-1]
    # print(line_series_data)

    res = {
        'status': True,
        'data': {
            'line_title_text': line_title_text,
            'line_xAxis_data': line_xAxis_data,
            'line_series_data': line_series_data,
        }
    }
    return JsonResponse(res)
