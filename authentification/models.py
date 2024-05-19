from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password

class AuthManager(BaseUserManager):
    def create_user(self, regNo, name, email, mobile, password):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(
            regNo=regNo,
            name=name,
            email=email,
            mobile=mobile
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, regNo, name, email, mobile, password):
        user = self.create_user(
            regNo=regNo,
            name=name,
            email=email,
            mobile=mobile,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Auth(AbstractBaseUser, PermissionsMixin):
    regNo = models.CharField(unique=True, max_length=500)
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, max_length=320)
    mobile = models.CharField(null=True, max_length=500)
    password = models.CharField(max_length=128, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='auth_users'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='auth_users'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['regNo', 'name', 'mobile']

    objects = AuthManager()

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_staff(self):
        return self.is_admin