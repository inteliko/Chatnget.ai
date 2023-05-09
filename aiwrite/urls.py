from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .  import views


urlpatterns = [
    path('', views.home, name="home"),
    path('registration', views.registration, name="Registration"),
    path('signin', views.signin, name="Signin"),
    path('signout', views.signout, name="Signout"),
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('dashboard/chatbot/', views.chatbot, name="chatbot"),
    path('subscription/dashboard/chatbot/', views.chatbot, name="chatbot"),
    path('subscription/dashboard/chatbot/imgtotxt/', views.chatbot, name="chatbot"),



    path('dashboard/imgtotxt/', views.imgtotxt, name="Image to Text"),
    path('subscription/dashboard/imgtotxt/', views.imgtotxt, name="Image to Text"),

    path('dashboard/img/<int:image_id>/download/', views.download_image, name='download_image'),




    path('subscription/', views.subscription, name='subscription'),
    # other URL patterns for your app...
    path('subscription/dashboard/', views.dashboard, name="Dashboard"),




]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
