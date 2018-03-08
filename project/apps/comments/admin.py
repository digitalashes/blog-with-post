from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'truncated_body', 'post_link',
        'author_link', 'ip_address',
        'created', 'modified',
    )
    list_display_links = ('truncated_body',)
    readonly_fields = (
        'created', 'modified',
    )
    search_fields = (
        'id', 'body',
        'post', 'user',
    )
    list_filter = ('ip_address',)
    list_select_related = ('user', 'post')
    raw_id_fields = ('user', 'post')

    def truncated_body(self, obj):
        return mark_safe(truncatechars(obj.body, 25))

    truncated_body.allow_tags = False
    truncated_body.short_description = mark_safe(_('Comment'))

    def post_link(self, obj):
        url = reverse('admin:posts_post_change', args=(obj.post_id,))
        return mark_safe(f'<a href="{url}">{escape(obj.post)}</a>')

    post_link.allow_tags = True
    post_link.short_description = mark_safe(_('Post'))

    def author_link(self, obj):
        url = reverse('admin:users_user_change', args=(obj.user_id,))
        return mark_safe(f'<a href="{url}">{escape(obj.user)}</a>')

    author_link.allow_tags = True
    author_link.short_description = mark_safe(_('Author'))
