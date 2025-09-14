from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role', 'first_name', 'last_name',
            'bio', 'created_at', 'updated_at', 'permissions', 'password'
        )
        read_only_fields = ('created_at', 'updated_at', 'permissions')
        
    def get_permissions(self, obj):
        return obj.get_permissions()
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("邮箱已存在")
        return value
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role='student'  # 注册用户默认为学生角色
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError("Invalid username or password")
                
            if not user.is_active:
                raise serializers.ValidationError("User is disabled")
                
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError("Both 'username' and 'password' are required")

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()