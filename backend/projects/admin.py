from django.contrib import admin
from .models import Profile, Message

admin.site.register(Profile)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'created_at')
    search_fields = ('subject', 'sender__username')
    list_filter = ('sender', 'created_at')
