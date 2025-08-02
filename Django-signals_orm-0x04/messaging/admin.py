from django.contrib import admin
from models import Message, Notification, MessageHistory

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('edited_at',)
    can_delete = False

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read', 'edited')
    list_filter = ('is_read', 'edited', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')
    inlines = [MessageHistoryInline]
    readonly_fields = ('timestamp', 'last_edited')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message__content')

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_at')
    list_filter = ('edited_at',)
    search_fields = ('content', 'message__id')
    readonly_fields = ('message', 'content', 'edited_at')