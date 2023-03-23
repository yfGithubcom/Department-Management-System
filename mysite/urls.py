"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app02.views import index, su, login, department, user, project, task, chart

urlpatterns = [
    path('admin/', admin.site.urls),
    # 主页
    path('', index.index),
    # 管理员用户
    path('su/list/', su.su_list),
    path('su/add/', su.su_add),
    path('su/<int:suid>/edit/', su.su_edit),
    path('su/<int:suid>/del/', su.su_del),
    path('su/<int:suid>/reset/', su.su_reset),
    # 登录和登出
    path('login/', login.login),
    path('img/code/', login.img_code),
    path('logout/', login.logout),
    # 部门管理
    path('department/list/', department.department_list),
    path('department/add/', department.department_add),
    path('department/del/', department.department_del),
    path('department/<int:did>/edit/', department.department_edit),
    # 员工管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),  # ModelForm方法
    path('user/<int:uid>/edit/', user.user_edit),
    path('user/<int:uid>/del/', user.user_del),
    # 项目管理
    path('project/list/', project.project_list),
    path('project/add/', project.project_add),
    path('project/<int:p_id>/edit/', project.project_edit),
    path('project/<int:p_id>/del/', project.project_del),
    # 任务管理
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),
    path('task/<int:tid>/del/', task.task_del),
    path('task/<int:tid>/edit/', task.task_edit),
    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),
    path('chart/line/', chart.chart_line),
]
