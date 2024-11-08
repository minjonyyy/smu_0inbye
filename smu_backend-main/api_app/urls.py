from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('', views.success, name='success'),
    path('success/', views.success, name='success'),
#    path('pdf/<str:pdf_file_name>/', views.get_pdf_file, name='get_pdf_file'),
 #path('upload/', views.upload_pdf, name='upload_pdf'),
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)