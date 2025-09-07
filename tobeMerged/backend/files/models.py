from django.db import models
import os
import uuid

def get_file_path(instance, filename):
    """生成唯一的文件路径"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class MediaFile(models.Model):
    """媒体文件模型"""
    FILE_TYPES = (
        ('video', '视频'),
        ('pdf', 'PDF'),
        ('other', '其他'),
    )
    
    title = models.CharField(max_length=255, verbose_name='标题')
    file = models.FileField(upload_to=get_file_path, verbose_name='文件')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='other', verbose_name='文件类型')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    file_size = models.BigIntegerField(default=0, verbose_name='文件大小(字节)')
    
    class Meta:
        verbose_name = '媒体文件'
        verbose_name_plural = '媒体文件'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.file_size and self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    @property
    def file_size_mb(self):
        """返回文件大小（MB）"""
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def file_extension(self):
        """返回文件扩展名"""
        return os.path.splitext(self.file.name)[1].lower()
