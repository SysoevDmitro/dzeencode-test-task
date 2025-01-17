from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=50,
        required=False,  # Обязательно только для анонимных пользователей
        allow_blank=True
    )
    email = serializers.EmailField(
        required=False,  # Обязательно только для анонимных пользователей
        allow_blank=True
    )
    replies = serializers.SerializerMethodField()  # Для вложенных комментариев

    class Meta:
        model = Comment
        fields = ['id', 'username', 'email', 'text', 'home_page', 'captcha', 'parent', 'created_at', 'replies']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """Валидация для анонимных пользователей"""
        user = self.context['request'].user
        if not user.is_authenticated:
            if not data.get('username'):
                raise serializers.ValidationError(
                    {"username": "Имя пользователя обязательно для анонимных пользователей."})
            if not data.get('email'):
                raise serializers.ValidationError({"email": "Email обязателен для анонимных пользователей."})
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['username'] = user.username
            validated_data['email'] = user.email
        return super().create(validated_data)

    def get_replies(self, obj):
        """Рекурсивно сериализуем дочерние комментарии"""
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
