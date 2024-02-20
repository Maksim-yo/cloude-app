from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

app_name = "accounts"

urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('signup/', views.SignupView.as_view(), name="signup")

]
