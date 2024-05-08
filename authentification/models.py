from django.contrib.auth.models import User
from django.db import models
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from datetime import timedelta

class Auth(models.Model):
    regNo = models.TextField(unique=True)
    name = models.TextField()
    email = models.TextField()
    mobile = models.TextField(null=True)
    password = models.CharField(max_length=400, null=True) 
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.email
    
    # generate jwt token
    def get_jwt_token_for_user(self):
            """ get jwt token for the user """
            refresh = RefreshToken.for_user(self)
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(days=7))
            return {            
                'access_token': str(access_token),
                'refresh_token': str(refresh),
            }