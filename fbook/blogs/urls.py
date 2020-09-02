from django.urls import path,include
from .import views
from .views import PostUpdateView,PostDeleteView

urlpatterns = [
    path("", views.home, name="home"),
    path("like/", views.likeUnlikePost, name="likeUnlikePost"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="postUpdate"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="postDelete")
    
]
