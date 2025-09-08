from django.contrib import admin
from .models import MediaFile

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """媒体文件管理界面"""
    list_display = ['title', 'file_type', 'file_size_mb', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at', 'file_size', 'file_size_mb', 'file_extension']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description')
        }),
        ('文件信息', {
            'fields': ('file', 'file_type')
        }),
        ('系统信息', {
            'fields': ('uploaded_at', 'file_size', 'file_size_mb', 'file_extension'),
            'classes': ('collapse',)
        }),
    )
