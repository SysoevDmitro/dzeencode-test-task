from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ как залогиненным, так и анонимным пользователям

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)  # Передаём текущего пользователя
        else:
            serializer.save()  # Сохраняем для анонимных
