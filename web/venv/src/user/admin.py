from django.contrib import admin
from user.models import CustomUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'guild', 'is_staff')
    list_filter = ('guild', 'is_staff', 'is_superuser')
    search_fields = ('username', 'guild', 'Implementation_rating', 'DP_rating', 'Graph_rating', 'Math_rating', 'DataStructure_rating', 'Greedy_rating')
    ordering = ('id',)

    fieldsets = [
        ('General', {'fields': ['username', 'email', 'password', 'guild', 'CF_handle']}),
        ('Authority', {'fields': ['is_staff', 'is_superuser']}),
        ('Rating', {'fields': ['Implementation_rating', 'DP_rating', 'Graph_rating', 'Math_rating', 'DataStructure_rating', 'Greedy_rating']}),
    ]

# Register your models here.
admin.site.register(CustomUser, UserAdmin)