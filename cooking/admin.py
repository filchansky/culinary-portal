from django.contrib import admin

from .models import Category, Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'watched', 'is_published', 'category')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    readonly_fields = ('watched',)
    list_filter = ('category',)


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
