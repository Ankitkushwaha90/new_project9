from rest_framework import serializers
from .models import Course, Module, Content

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'content', 'order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ModuleSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'contents', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'modules', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']
