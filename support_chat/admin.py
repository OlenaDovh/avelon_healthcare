from django.contrib import admin
from .models import SupportChatMessage, SupportChatSession

class SupportChatMessageInline(admin.TabularInline):
    """Описує клас `SupportChatMessageInline`."""
    model = SupportChatMessage
    extra = 0
    readonly_fields = ('author_type', 'author_name', 'text', 'created_at')
    can_delete = False

@admin.register(SupportChatSession)
class SupportChatSessionAdmin(admin.ModelAdmin):
    """Описує клас `SupportChatSessionAdmin`."""
    list_display = ('id', 'customer_display_name', 'topic', 'status', 'operator', 'created_at')
    list_filter = ('status', 'topic', 'created_at')
    search_fields = ('guest_name', 'guest_email', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'connected_at', 'closed_at')
    inlines = [SupportChatMessageInline]
