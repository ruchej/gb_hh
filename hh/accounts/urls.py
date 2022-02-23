from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import Login, Logout, UserCreate, UserConfirm, UserDetail, ProfileUpdateView, favourites_add

app_name = "accounts"

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("singup/", UserCreate.as_view(), name="user-create"),
    path("confirm/<uidb64>/<token>/", UserConfirm.as_view(), name="user-confirm"),
    path("editeprof/", ProfileUpdateView.as_view(), name="profile-update"),
    path("", UserDetail.as_view(), name="user-detail"),
    path("fav/<int:id>/", favourites_add, name="favourite_add"),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(email_template_name='accounts/password_reset_email.html',
                                              success_url=reverse_lazy('accounts:password_reset_done'),
                                              template_name='accounts/password_reset_form.html'),
         name='password_reset'),
    path('password_reset_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete'),
                                                     template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
