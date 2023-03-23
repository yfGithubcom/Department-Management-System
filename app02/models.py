from django.db import models


# Create your models here.
class Su(models.Model):
    # 管理员
    su = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)


class Department(models.Model):
    # 部门表
    unit = models.CharField(verbose_name='部门名称', max_length=32, unique=True)
    mobile = models.CharField(verbose_name='部门电话', max_length=16, blank=True)

    def __str__(self):
        return self.unit


class User(models.Model):
    # 员工表
    user = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    salary = models.IntegerField(verbose_name='薪水')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    unit = models.ForeignKey(verbose_name='单位', to='Department', to_field='id',
                             on_delete=models.CASCADE)  # 级联删除 xxx_id 数据库field会自动带上_id
    entry_date = models.DateField(verbose_name='入职时间', default='1999-01-01')
    # xxx = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)  # 置空
    gender_choices = ((1, '男'), (2, '女'))  # 在django内部做约束
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    def __str__(self):
        return self.user


class Project(models.Model):
    # 项目/工程表
    name = models.CharField(verbose_name='项目', max_length=64)
    budget = models.IntegerField(verbose_name='预算')
    level_choices = ((1, 'A级'), (2, 'B级'), (3, 'C级'))
    level = models.SmallIntegerField(verbose_name='等级', choices=level_choices, default=3)
    status_choices = ((1, '未启动'), (2, '进行中'), (3, '待交付'), (4, '已结束'))
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    def __str__(self):
        return self.name


class Task(models.Model):
    # 任务
    title = models.CharField(verbose_name='标题', max_length=64)
    level_choices = ((1, '紧急'), (2, '重要'), (3, '一般'))
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=3)
    user = models.ForeignKey(verbose_name='负责人', to=User, to_field='id', null=True, blank=True,
                             on_delete=models.SET_NULL)
    project = models.ForeignKey(verbose_name='所属项目', to=Project, to_field='id', on_delete=models.CASCADE)
    leader = models.ForeignKey(verbose_name='领导', to=Su, to_field='id', null=True, blank=True,
                               on_delete=models.SET_NULL)
    detail = models.TextField(verbose_name='任务详情')
