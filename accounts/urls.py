from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from . import views
urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name="profile"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup/', views.SignupView.as_view(), name="signup")

    # Страница авторизации.
    # path('register/', views.register,
    #     name='register'),
]
