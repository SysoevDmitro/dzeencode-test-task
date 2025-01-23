from django.urls import path


from .views import CommentListCreateView, index

app_name = "comments"

urlpatterns = [
    path('', index, name="index"),
    path("api/comments/", CommentListCreateView.as_view(), name="comments"),
]
