from django.contrib import admin

from users.models import User, Payments


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('email',)
    ordering = ("id",)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user',)
    ordering = ("id",)
