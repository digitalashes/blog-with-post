from allauth.account.models import EmailAddress
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm as UserChangeFormBase
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from common.utils import get_object_or_none

admin.site.unregister(Group)
User = get_user_model()


class EmailAddressStackedInline(admin.StackedInline):
    model = EmailAddress
    fields = ('email', 'verified', 'primary',)
    extra = 0


class UserChangeForm(UserChangeFormBase):
    class Meta(UserChangeFormBase.Meta):
        model = User
        fields = '__all__'


class UserCreationForm(UserCreationFormBase):
    error_message = UserCreationFormBase.error_messages.update({
        'duplicate_username': 'This username has already been taken.',
        'duplicate_email': 'This email has already been taken.',
    })

    class Meta(UserCreationFormBase.Meta):
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        obj = get_object_or_none(User, username=username)
        if obj:
            raise forms.ValidationError(self.error_messages.get('duplicate_username'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        obj = get_object_or_none(User, email=email)
        if obj:
            raise forms.ValidationError(self.error_messages.get('duplicate_email'))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        EmailAddress.objects.create(user=user,
                                    email=user.email,
                                    primary=True)
        return user


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    inlines = (EmailAddressStackedInline,)
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'is_active', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {
            'fields': (
                'username', 'email',
                'first_name', 'last_name',
                'avatar',
                'password', 'last_login', 'date_joined'
            )
        }),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        })
    )
