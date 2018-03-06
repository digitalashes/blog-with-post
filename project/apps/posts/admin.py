from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from posts.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author_link', 'status'
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

    def author_link(self, obj):
        url = reverse('admin:users_user_change', args=(obj.author_id,))
        return mark_safe(f'<a href="{url}">{escape(obj.author)}</a>')

    author_link.allow_tags = True
    author_link.short_description = mark_safe(_('Author'))
