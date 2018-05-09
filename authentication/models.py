from django.db import models
import bcrypt

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, age=None, country=None, salt=None, is_active=True, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not email:
            raise ValueError("Users must have a password")

        user_obj = User(email=email, age=age, country=country)

        salt = bcrypt.gensalt()
        user_obj.salt = salt.decode('ascii')
        hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
        user_obj.password = hashed_password.decode('ascii')
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    age = models.IntegerField(default=0)
    country = models.CharField(max_length=50)
    salt = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [email, age, country]
    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active