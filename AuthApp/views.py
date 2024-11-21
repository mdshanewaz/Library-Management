from django.shortcuts import render
from AuthApp.models import CustomUser
from AuthApp.serializers import CustomUserSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
