from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('login_module.urls')),
    path('', include('board.urls')),
    path('chat/', include('chat.urls')),
    path('', include('kakaopay.urls')),
    path('', include('api_app.urls')),
]
