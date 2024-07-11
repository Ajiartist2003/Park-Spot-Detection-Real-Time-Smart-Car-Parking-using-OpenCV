from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm


urlpatterns = [
    path('', views.home),
    path('video/', views.video_feed, name='video'),
    path('contact/',views.contact, name='contact'),
    
    
    #authentication
    path('accounts/login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm,next_page='/'), name='login'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)