from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    TEACHER = 'teacher', _('Teacher')
    STUDENT = 'student', _('Student')

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT
    )
    bio = models.TextField(_('biography'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 添加权限映射
    def get_permissions(self):
        """根据用户角色返回对应的权限列表"""
        permissions_map = {
            'admin': [
                'view_users', 'create_users', 'update_users', 'delete_users',
                'view_courses', 'create_courses', 'update_courses', 'delete_courses',
                'view_documents', 'create_documents', 'update_documents', 'delete_documents',
                'view_exams', 'create_exams', 'update_exams', 'delete_exams',
                'view_results', 'manage_system'
            ],
            'teacher': [
                'view_users', 'view_courses', 'create_courses', 'update_courses', 'delete_courses',
                'view_documents', 'create_documents', 'update_documents', 'delete_documents',
                'view_exams', 'create_exams', 'update_exams', 'delete_exams',
                'view_results'
            ],
            'student': [
                'view_courses', 'view_documents', 'view_exams', 'take_exams', 'view_results'
            ]
        }
        return permissions_map.get(self.role, [])
    
    def __str__(self):
        return f'{self.username} ({self.role})'
