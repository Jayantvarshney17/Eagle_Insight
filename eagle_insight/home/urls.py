from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('user/', views.user, name='user'),
    path('forgot/', views.forgot, name='forgot'),
    path('forgotton/', views.forgotton, name='forgotton'),
    path('officer_Owner/', views.officer_Owner, name='officer_Owner'),
    path('get_status/', views.get_status, name='get_status'),   
    path('live/', views.live, name='live'),   
    path('processed_video_feed/', views.stream_processed_video, name='processed_video_feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)