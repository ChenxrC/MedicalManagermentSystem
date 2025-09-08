from rest_framework import serializers
from .models import MediaFile

class MediaFileSerializer(serializers.ModelSerializer):
    """媒体文件序列化器"""
    file_size_mb = serializers.ReadOnlyField()
    file_extension = serializers.ReadOnlyField()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaFile
        fields = [
            'id', 'title', 'file', 'file_type', 'description', 
            'uploaded_at', 'file_size', 'file_size_mb', 
            'file_extension', 'file_url'
        ]
        read_only_fields = ['id', 'uploaded_at', 'file_size', 'file_size_mb', 'file_extension', 'file_type']
    
    def get_file_url(self, obj):
        """获取文件URL"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None
    
    def validate_file(self, value):
        """验证文件类型"""
        if value:
            # 检查文件扩展名
            allowed_video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
            allowed_pdf_extensions = ['.pdf']
            
            file_extension = value.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_video_extensions + allowed_pdf_extensions):
                raise serializers.ValidationError("只支持视频文件(.mp4, .avi, .mov, .wmv, .flv, .webm, .mkv)和PDF文件(.pdf)")
            
            # 检查文件大小 (50MB限制)
            if value.size > 50 * 1024 * 1024:
                raise serializers.ValidationError("文件大小不能超过50MB")
        
        return value
    
    def create(self, validated_data):
        """创建时自动设置文件类型"""
        file_obj = validated_data.get('file')
        if file_obj:
            file_extension = file_obj.name.lower()
            if file_extension.endswith('.pdf'):
                validated_data['file_type'] = 'pdf'
            else:
                validated_data['file_type'] = 'video'
        
        return super().create(validated_data)
