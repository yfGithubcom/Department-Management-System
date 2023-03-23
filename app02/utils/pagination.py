"""
自定义的分页组件

使用需知：
1.筛选自己的数据
    query_set = models.YourInstance.objects.filter()

2.实例化分页对象
    page_obj = pagination.Pagination(request,query_set)

3.返回 数据 和 分页导航栏
    page_query_set = page_obj.page_query_set
    page_list = page_obj.show_html()
    return render(request, 'xxx.html', {'page_query_set':page_query_set, 'page_list':page_list})

4.在 html 页面中
    {% for obj in page_query_set %}
        {{ obj.x1 }}
        {{ obj.x2 }}
        ...
    {% endfor% }

    <ul class='pagination'>
        {{ page_list }}
    </ul>
"""

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, query_set, page_size=10, page_param='page', plus=2):
        """
        :param request: 请求的对象
        :param query_set: 符合条件的数据集合
        :param page_size: 每一页展示的数据
        :param page_param: 在url中传递的，获取页码的参数，比如：http://127.0.0.1:8000/user/list/?page=1 中为 'page'
        :param plus: 显示当前页的前/后几页
        """
        from django.http.request import QueryDict
        import copy

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        # 每一页展示数据的索引
        self.start = page_size * (page - 1)
        self.end = page_size * page
        # 计算总页码
        total = query_set.count()  # 数据总条数
        total_page, remainder = divmod(total, page_size)
        if remainder:
            total_page += 1
        self.total_page = total_page
        self.plus = plus  # 指定页数的左右跨度
        self.page_query_set = query_set[self.start: self.end]  # 每页展示obj的起始索引和终止索引

    def show_html(self):
        page_list = []
        if self.total_page <= 2 * self.plus + 1:  # 总页数比较少的时候
            s_page, e_page = 1, self.total_page
        else:
            if self.page <= self.plus:
                s_page, e_page = 1, 2 * self.plus + 1
            else:
                if self.page <= self.total_page - self.plus:
                    s_page = self.page - self.plus
                    e_page = self.page + self.plus
                else:
                    s_page = self.total_page - 2 * self.plus
                    e_page = self.total_page

        # 上一页按钮
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            previous_page = f"<li><a href='?{self.query_dict.urlencode()}'>上一页</a></li>"
        else:
            self.query_dict.setlist(self.page_param, [1])
            previous_page = f"<li><a href='?{self.query_dict.urlencode()}'>上一页</a></li>"
        page_list.append(previous_page)
        # 页码按钮
        for i in range(s_page, e_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                page_switch = f"<li class='active'><a href='?{self.query_dict.urlencode()}'>{i}</a></li>"
            else:
                page_switch = f"<li><a href='?{self.query_dict.urlencode()}'>{i}</a></li>"
            page_list.append(page_switch)
        # 下一页按钮
        if self.page < self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next_page = f"<li><a href='?{self.query_dict.urlencode()}'>下一页</a></li>"
        else:
            self.query_dict.setlist(self.page_param, [self.total_page])
            next_page = f"<li><a href='?{self.query_dict.urlencode()}'>下一页</a></li>"
        page_list.append(next_page)
        # 序列化 & mark_safe
        page_list = mark_safe(''.join(page_list))
        return page_list
