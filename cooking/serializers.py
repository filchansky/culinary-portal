from rest_framework import serializers

from .models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    """Fields displayed in API."""

    class Meta:
        model = Category
        fields = ('title', 'id')


class PostSerializer(serializers.ModelSerializer):
    """Fields displayed in API."""

    class Meta:
        model = Post
        fields = ('title', 'category', 'created_at', 'content', 'author')
