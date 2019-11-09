from django import template

from ..models import Post, Category, Tag

register = template.Library()


# 要成为一个可用的 tag 库，模块必须包含一个名为 register 的模块级变量，
# 它是一个 template.Library 实例。所有的 tags 和 filters 均在其中注册

# 这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，并将函数 show_recent_posts 装饰为 register.inclusion_tag，这样就告诉
# django，这个函数是我们自定义的一个类型为 inclusion_tag 的模板标签。
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


# inclusion_tag 装饰器的参数 takes_context 设置为 True 时将告诉 django，在渲染 _recent_posts.html 模板时，不仅传入show_recent_posts
# 返回的模板变量，同时会传入父模板（即使用 {% show_recent_posts %} 模板标签的模板）上下文（可以简单理解为渲染父模板的视图函数传入父模板的模板变量以及 django 自己传入的模板变量）。
# show_recent_posts 标签可以接收参数，默认为 5，即显示 5 篇文章，如果要控制其显示 10 篇文章，可以使用 {% show_recent_posts 10 %} 这种方式传入参数。


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context, num=5):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
        # 这里 Post.objects.dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间（已去重），且是
        # Python的date对象，精确到月份，降序排列。接受的三个参数值表明了这些含义，一个是created_time ，
        # 即Post的创建时间，month是精度，order = 'DESC'表明降序排列（即离当前越近的时间越排在前面）。
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }
