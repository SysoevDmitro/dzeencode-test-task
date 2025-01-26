from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken
from .models import Comment
from .forms import CommentForm
from .serializers import CommentSerializer
from rest_framework.permissions import AllowAny


class CommentPagination(PageNumberPagination):
    page_size = 25


def get_user_from_token(token):
    """Достает юзера из куки"""
    access_token = AccessToken(token)
    user_id = access_token.payload.get('user_id')

    if not user_id:
        raise AuthenticationFailed('User ID not found in token')
    return user_id


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
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
        form_data = request.session.pop('form_data', None)
        form_errors = request.session.pop('form_errors', None)
        comments = self.get_queryset()

        paginator = CommentPagination()
        paginated_comments = paginator.paginate_queryset(comments, request)

        commen = []
        token = request.COOKIES.get('access_token')

        for comment in paginated_comments:
            if comment.file:
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
            return render(request, "comments.html", {'form': form, 'comments': paginated_comments,
                                                 'commen': commen, 'user': user, 'form_errors': form_errors, 'form_data': form_data})
        return render(request, "comments.html", {'form': form, 'comments': paginated_comments,
                                                 'commen': commen})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        response = redirect("/api/comments/")
        if form.is_valid():
            form.save()
            return response

        # Если форма не валидна
        request.session['form_data'] = request.POST.dict()
        form_errors = [str(error) for errors in form.errors.values() for error in errors]
        request.session['form_errors'] = form_errors
        return response


def index(request):
    return render(request, "base.html")
