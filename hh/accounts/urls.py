from django.urls import path, reverse_lazy

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
]
