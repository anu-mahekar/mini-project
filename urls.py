# birds/urls.py
from django.urls import path
from .views import (
    PredictView, RegisterView, LoginView, LogoutView,
    UserView, HistoryView
)

urlpatterns = [
    path("predict/", PredictView.as_view(), name="predict"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
    path("history/", HistoryView.as_view(), name="history"),
]

