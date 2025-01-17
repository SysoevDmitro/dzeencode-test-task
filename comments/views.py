from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    paginate_by = 25
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Получаем параметры сортировки из запроса
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        order = self.request.query_params.get('order', 'asc')

        if order == 'desc':
            sort_by = f'-{sort_by}'

        # Возвращаем отсортированные комментарии
        return Comment.objects.filter(parent=None).order_by(sort_by)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()
