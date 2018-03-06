from django.contrib import admin

from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'status'
    )
    list_display_links = ('title',)
    readonly_fields = (
        'status_changed',
        'created', 'modified',
    )
    search_fields = (
        'id', 'title', 'body',
    )
    list_filter = ('status',)
    list_select_related = ('author',)
    raw_id_fields = ('author',)
