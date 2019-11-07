import mistune
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post


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
    post.body = mistune.markdown(post.body)
    return render(request, 'blog/detail.html', context={'post': post})

