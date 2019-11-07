from django.apps import AppConfig


# 在BlogConfig类中对app做了一些配置，所以应该将这个类注册进去
class BlogConfig(AppConfig):
    name = 'blog'
    # 修改app在admin后台的显示名字
    verbose_name = '博客'
