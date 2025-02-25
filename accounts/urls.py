from django.urls import path, include
from rest_framework import routers

from accounts import viewsets

router = routers.SimpleRouter()

# Rota para Users CRUD
router.register(r"users", viewsets.UserViewSet, basename="user")

urlpatterns = [
    # Inclui todas as rotas do roteador na raiz ('').
    path("", include(router.urls)),
    path("login/", viewsets.LoginView.as_view(), name="login"),
    path("search/", viewsets.UserSearchViewSet.as_view({"get": "list"}), name="search")
]
