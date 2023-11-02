from django.contrib import admin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'is_blocked',
        'is_superuser',
    )
    list_filter = (
        'email', 'username', 'is_blocked', 'is_superuser',
    )
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    fieldsets = (
        (None, {'fields': (
            'email', 'username', 'first_name', 'last_name', 'password',
        )}),
        ('Permissions', {'fields': ('is_blocked', 'is_superuser',)})
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
