from django.urls import path
from django.contrib.auth import views as auth_views


from . import views
urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('signup/', views.SignupView.as_view(), name="signup")

]
