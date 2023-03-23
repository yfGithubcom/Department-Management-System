from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app02.models import Department, User, Project, Su, Task
from app02.utils.encrypt import md5


class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加样式
        for name, field in self.fields.items():
            # if name == 'account':  # 设置某个字段不添加样式
            #     continue
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


class BootstrapForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


class DepartmentModelForm(BootstrapModelForm):
    reg = [RegexValidator(r'^1\d{10}$|^\d{7}$', message='电话格式错误')]  # 号码格式验证 方法1（正则）
    mobile = forms.CharField(label='部门电话', validators=reg)

    class Meta:
        model = Department
        fields = '__all__'

    # def clean_mobile(self):  # 号码验证 方法2（钩子方法）
    #     mobile = self.cleaned_data['mobile']
    #     exists = Department.objects.exclude(id=self.instance.pk).filter(mobile=mobile).exists()
    #     if exists:
    #         raise ValidationError('电话号码已存在')
    #     if len(mobile) not in [7, 11]:
    #         raise ValidationError('电话格式错误')
    #     return mobile


class UserModelForm(BootstrapModelForm):
    user = forms.CharField(min_length=2, label='姓名')  # 重写user属性，对form字段做限制

    class Meta:
        model = User
        fields = ['user', 'age', 'salary', 'account', 'gender', 'unit', 'entry_date']
        # widgets = {
        #     'user': forms.TextInput(attrs={'class': 'form-control'}), ...
        # }


class ProjectModelForm(BootstrapModelForm):
    class Meta:
        model = Project
        # fields = ['id', 'name', 'budget', 'level', 'status']
        fields = '__all__'  # form包含所有字段
        # exclude = []  # 排除的字段


class SuModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(label='密码确认', widget=forms.PasswordInput)  # render_value=True

    class Meta:
        model = Su
        fields = ['su', 'password', 'confirm_password']
        widgets = {'password': forms.PasswordInput}

    def clean_password(self):  # md5加密
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError('密码不一致')
        return confirm_pwd


class SuEditModelForm(BootstrapModelForm):
    class Meta:
        model = Su
        fields = ['su']


class SuResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(label='密码确认', widget=forms.PasswordInput)

    class Meta:
        model = Su
        fields = ['password', 'confirm_password']
        widgets = {'password': forms.PasswordInput}

    def clean_password(self):  # md5加密
        pwd = self.cleaned_data.get('password')
        # 校验重置的密码是否和修改前相同
        exists = Su.objects.filter(id=self.instance.pk, password=md5(pwd)).exists()
        if exists:
            raise ValidationError('密码未作修改')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm_pwd:
            raise ValidationError('密码不一致')
        return confirm_pwd


class LoginForm(BootstrapForm):
    su = forms.CharField(label='用户名', widget=forms.TextInput, required=True)  # required=True 设置不能为空（默认）
    password = forms.CharField(label='密码', widget=forms.PasswordInput, required=True)
    img_code = forms.CharField(label='请输入验证码')

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['leader']
