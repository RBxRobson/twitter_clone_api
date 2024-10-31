from django.urls import path, include
from rest_framework import routers

from accounts import viewsets

router = routers.SimpleRouter()

# Rota para Users CRUD
router.register(r"users", viewsets.UserViewSet, basename="user")

urlpatterns = [
    # Inclui todas as rotas do roteador na raiz ('').
    path("", include(router.urls))
]
