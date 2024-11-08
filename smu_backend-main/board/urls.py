from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('post/', views.PostList.as_view()),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('post/update-latest/', views.UpdateLatestPostView.as_view(), name='update-latest-post'),
    path('post-image/', views.PostImageCreateView.as_view(), name='post-image-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)