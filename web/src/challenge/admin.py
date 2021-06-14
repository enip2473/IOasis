from django.contrib import admin
from challenge.models import Challenge

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'CF_handle', 'guild', 'ProblemName')
    search_fields = ('guild', 'CF_handle', 'username', 'ProblemName')
    ordering = ('id', )

    fieldsets = [
        ('UserSetting', {'fields': ['guild', 'username', 'CF_handle']}),
        ('ProblemSetting', {'fields': ['ProblemName', 'Difficulty', 'Time']}),
    ]

# Register your models here.
admin.site.register(Challenge, ChallengeAdmin)