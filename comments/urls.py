from django.urls import path


from .views import CommentListCreateView

app_name = "comments"

urlpatterns = [
    path("comments/", CommentListCreateView.as_view(), name="comments-list-create")
]
