from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def _create(self, email, username,  password, **extra):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('you have not entered username')
        if not email:
            raise ValueError('you have not entered email')
        user = self.model(
            email=self.normalize_email(email),
            username=username, **extra
        )
        user.set_password(raw_password=password)
        user.save(using=self.db)

    def create(self, email, username, password):
        return self._create(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create(email, username, password, is_staff=True, is_superuser=True)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(blank=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='users/avatar', blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username


class UserRating(models.Model):
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey('product.RatingStar',
                             on_delete=models.CASCADE, verbose_name="star")
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="username",
                                 related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.username}"
