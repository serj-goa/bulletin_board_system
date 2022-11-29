from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Ad, Category, Location, User


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'category', 'name', 'author', 'price', 'is_published'
    ]
    list_display_links = ['name', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name'
    ]
    list_display_links = ['name', ]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'address', 'latitude', 'longitude'
    ]
    list_display_links = ['address', ]


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = [
        'username', '_full_name', 'email', 'role', 'age', 'location', 'is_active', 'is_staff', 'is_superuser'
    ]
    list_display_links = ['username', ]

    def _full_name(self, obj: User):
        return obj.full_name

    _full_name.short_description = _('Full name')
