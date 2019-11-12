import re

import markdown
from markdown.extensions.toc import TocExtension
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.utils.text import slugify


# Create your views here.


def index(request):
    # 这个 request 就是 django 为我们封装好的 HTTP 请求，它是类 HttpRequest 的一个实例。
    # return HttpResponse("欢迎访问我的博客首页！")
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'post_list': post_list,
        'welcome': '欢迎访问我的博客首页',
    })


# def render(request: Any,
#            template_name: Any,
#            context: Any = None,
#            content_type: Any = None,
#            status: Any = None,
#            using: Any = None) -> HttpResponse


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increse_post_view()  # 阅读量加一
    # post.body = mistune.markdown(post.body) mistune也可以
    # post.body = markdown.markdown(post.body, extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',  # 语法高亮拓展
    #     'markdown.extensions.toc',  # 自动生成目录的拓展
    # ])
    # 这里markdown对代码块的支持不太好，缩进4个空格/1tab只有<pre></pre>而没有<code></code>
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        TocExtension(slugify=slugify)  # TocExtension 的实例,Markdown 内置的处理方法不能处理中文标题，所以我们使用了 django.utils.text 中的
        # slugify 方法，该方法可以很好地处理中文。
    ])
    post.body = md.convert(post.body)
    content = re.search(r'<ul>(.*)</ul>', md.toc, re.S)  # re.S表示.匹配所有字符包括\n
    post.toc = md.toc  # 实现在任何都能生成目录，无需[TOC]
    if content.group(1) is '':
        post.toc = ''
    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    # 这里created_time是Python的date对象，其有一个year和month属性
    # Python中调用属性的方式通常是created_time.year，但是由于这里作为方法的参数列表，所以django要求我们把点替换成了两个下划线，即created_time__year
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
