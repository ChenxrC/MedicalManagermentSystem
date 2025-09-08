from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MediaFile
from .serializers import MediaFileSerializer

class MediaFileViewSet(viewsets.ModelViewSet):
    """媒体文件视图集"""
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    pagination_class = None  # 禁用分页，返回所有文件
    
    def get_queryset(self):
        """根据文件类型过滤"""
        print("Getting queryset...")
        queryset = MediaFile.objects.all()
        print(f"Total files in database: {queryset.count()}")
        
        # 打印所有文件的信息
        for file in queryset:
            print(f"File: {file.title}, Type: {file.file_type}, ID: {file.id}")
        
        file_type = self.request.query_params.get('file_type', None)
        if file_type:
            queryset = queryset.filter(file_type=file_type)
            print(f"Filtered by type '{file_type}': {queryset.count()}")
        result = queryset.order_by('-uploaded_at')
        print(f"Returning {result.count()} files")
        return result
    
    def list(self, request, *args, **kwargs):
        """重写list方法以确保request上下文正确传递"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def videos(self, request):
        """获取所有视频文件"""
        videos = MediaFile.objects.filter(file_type='video').order_by('-uploaded_at')
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pdfs(self, request):
        """获取所有PDF文件"""
        pdfs = MediaFile.objects.filter(file_type='pdf').order_by('-uploaded_at')
        serializer = self.get_serializer(pdfs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete_file(self, request, pk=None):
        """删除文件"""
        media_file = get_object_or_404(MediaFile, pk=pk)
        media_file.delete()
        return Response({'message': '文件删除成功'}, status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request, *args, **kwargs):
        """创建文件记录"""
        print("Received data:", request.data)
        print("Received files:", request.FILES)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
