from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Comment
from .forms import CommentForm
from .serializers import CommentSerializer
from rest_framework.permissions import AllowAny


class CommentPagination(PageNumberPagination):
    page_size = 25


def get_user_from_token(token):
    # Декодируем токен
    access_token = AccessToken(token)

    # Извлекаем user_id из payload
    user_id = access_token.payload.get('user_id')

    if not user_id:
        raise AuthenticationFailed('User ID not found in token')

    # Возвращаем user_id или можно использовать его для извлечения пользователя из базы данных
    return user_id

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Ограничиваем список полей для сортировки
        allowed_sort_fields = ['username', 'email', 'created_at']
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        order = self.request.query_params.get('order', 'asc')

        if sort_by not in allowed_sort_fields:
            sort_by = 'created_at'

        if order == 'desc':
            sort_by = f'-{sort_by}'

        return Comment.objects.filter(parent=None).order_by(sort_by)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            serializer.save(user=user)
        else:
            serializer.save()

    def get(self, request, *args, **kwargs):
        form = CommentForm()
        comments = self.get_queryset()
        commen = []
        token = request.COOKIES.get('access_token')

        for comment in comments:
            if comment.file:
                # Добавляем информацию о типе файла в контекст
                if comment.file.name.endswith(('.jpg', '.png', '.gif')):
                    comment.file_type = 'image'
                elif comment.file.name.endswith('.txt'):
                    comment.file_type = 'text'
                else:
                    comment.file_type = 'other'
            else:
                comment.file_type = None

            commen.append(comment)

        if token:
            user_id = get_user_from_token(token)
            user = get_user_model().objects.get(id=user_id)
            return render(request, "comments.html", {'form': form, 'comments': comments,
                                                 'commen': commen, 'user': user})
        return render(request, "comments.html", {'form': form, 'comments': comments,
                                                 'commen': commen})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)  # Используем данные из POST-запроса
        if form.is_valid():
            file = form.cleaned_data.get('file')
            if file:
                # Проверка размера для текстового файла
                if file.name.endswith('.txt'):
                    if file.size > 100 * 1024:  # Максимум 100 KB
                        form.add_error('file', 'File size must be less than 100KB.')
                # Проверка для изображений
                elif file.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    try:
                        img = Image.open(file)
                        if img.width > 320 or img.height > 240:
                            # Сжимаем изображение пропорционально
                            img.thumbnail((320, 240))
                            buffer = BytesIO()
                            img.save(buffer, format=img.format)
                            buffer.seek(0)
                            file = InMemoryUploadedFile(
                                buffer, None, file.name, file.content_type, buffer.tell(), None
                            )
                            form.cleaned_data['file'] = file
                    except Exception:
                        form.add_error('file', 'Invalid image file.')
                else:
                    form.add_error('file', 'Invalid file type. Allowed: .txt, .jpg, .jpeg, .png, .gif.')

            # Если ошибок нет, сохраняем комментарий
            if not form.errors:
                form.save()
                return redirect("/api/comments/")  # Перенаправление после сохранения

        # Если форма не валидна, возвращаем ошибку
        comments = self.get_queryset()
        return render(request, "comments.html", {
            'form': form,
            'comments': comments,
            'user': request.user,
            'error': 'Invalid data submitted'
        })


def index(request):
    return render(request, "base.html")
