from django.contrib import admin

# Register your models here.
from .models import Post, Tag, Category


class PostAdmin(admin.ModelAdmin):
    # 显示更加详细的信息，这需要我们来定制admin
    # fields中定义的字段就是表单中展现的字段
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)  # 注册
admin.site.register(Tag)
admin.site.register(Category)
