from django.urls import path

from .views import Login, Logout, UserCreate, UserConfirm, UserDetail


app_name = "accounts"

urlpatterns = [
    path("login/", Login.as_view(), name="Login"),
    path("logout/", Logout.as_view(), name="Logout"),
    path("singup/", UserCreate.as_view(), name="UserCreate"),
    path("confirm/<uidb64>/<token>/", UserConfirm.as_view(), name="UserConfirm"),
    path("", UserDetail.as_view(), name="UserDetail"),
]
