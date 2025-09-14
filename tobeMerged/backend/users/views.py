from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, LoginResponseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """根据不同的操作设置不同的权限"""
        if self.action in ['list', 'create', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'register':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'login':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'me':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """用户注册接口"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': '用户注册成功'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """用户登录接口"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            # 准备登录响应数据
            response_serializer = LoginResponseSerializer({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user
            })
            
            return Response({
                'message': 'User logged in successfully',
                'data': response_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """获取当前用户信息"""
        user = request.user
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data
        }, status=status.HTTP_200_OK)
        
    def list(self, request):
        """获取用户列表"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)
        
    def create(self, request):
        """创建用户（仅限管理员）"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '用户创建成功',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        """更新用户信息"""
        try:
            user = User.objects.get(pk=pk)
            
            # 检查权限：管理员可以更新任何用户，普通用户只能更新自己
            if not request.user.is_superuser and request.user != user:
                return Response({'message': '您没有更新此用户信息的权限'}, status=status.HTTP_403_FORBIDDEN)
                
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': '用户信息更新成功',
                    'user': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)
