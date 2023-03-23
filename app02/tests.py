from django.test import TestCase

# Create your tests here.

import random
from app02.models import User, Project

""" test1 """
# for i in range(70):
#     User.objects.create(
#         user=f'tester{i}',
#         age=random.randint(18, 35),
#         salary=1000 * random.randint(3, 8),
#         account=0,
#         unit_id=random.choice(dpt_id_lst),
#         gender=random.randint(1, 2),
#     )

""" test2 """
# for i in range(30):
#     Project.objects.create(
#         name=f'测试项目{i}',
#         budget=1000 * random.randint(1, 100),
#         level=random.randint(1, 3),
#         status=random.randint(1, 4),
#     )
