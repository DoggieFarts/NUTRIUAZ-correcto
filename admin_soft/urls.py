from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .serializers import EncuestaSerializer
from .views import EncuestaView, RegisterView, ActivateView

urlpatterns = [
    path('', views.index, name='index'),
    path('encuestas/', views.encuestas_view, name='encuestas'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('profile/', views.profile, name='profile'),
    path('encuesta/<int:encuesta_id>/seleccionar_grupo/', views.seleccionar_grupo, name='seleccionar_grupo'),
    path('encuesta/<int:encuesta_id>/realizar_encuesta/', views.realizar_encuesta, name='realizar_encuesta'),
    path('anova/', views.anova, name='anova'),
    path('api/encuesta/', EncuestaView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/activate/<str:username>/', ActivateView.as_view()),
    path('inactive_users/', views.inactive_users, name='inactive_users'),
    path('activate_user/<str:username>/', views.activate_user, name='activate_user'),
    path('encuestadores/', views.encuestadores, name='encuestadores'),



    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
