from django.contrib import admin

from user.models import UserRating, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'avatar',  'email', 'created_date')
    search_fields = ('id', 'username')
    ordering = ('-created_date',)


admin.site.register(User, UserAdmin)

admin.site.register(UserRating)