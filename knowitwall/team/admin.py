from django.contrib import admin
from django.utils.html import format_html
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'thumbnail']

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="%s" style="height: 50px; width: auto">' % (obj.image.url))
        else:
            "no image"
    thumbnail.short_description = 'Le team member'
