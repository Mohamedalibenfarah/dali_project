from django.urls import path
from .api import AuthCreateApi, AuthGetApi, AuthUpdateApi, AuthDeleteApi, AuthLoginApi

urlpatterns = [path ('api/create', AuthCreateApi.as_view ()),
               path ('api/login', AuthLoginApi.as_view ()),
               path ('api', AuthGetApi.as_view ()),
               path ('api/update', AuthUpdateApi.as_view ()),
               path ('api/delete', AuthDeleteApi.as_view ())]