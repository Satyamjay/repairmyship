from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# UserManager class extended from BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, age=None, country=None, is_active=True, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not email:
            raise ValueError("Users must have a password")

        """user_obj = User(email=email, age=age, country=country)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        salt = bcrypt.gensalt()
        user_obj.salt = salt.decode('ascii')
        hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
        user_obj.password = hashed_password.decode('ascii')"""
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.age = age
        user.country = country
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, age=None, country=None, is_admin=False, is_staff=True, is_active=True):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            age=age,
            country=country,
            is_staff=is_staff,
            is_admin=is_admin,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, age, country):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.age = age
        user.country = country
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


# My Custom User Model extended from Abstract Base User
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.NullBooleanField(default=False, null=True) # a admin user; non super-user
    age = models.IntegerField(default=0)
    country = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age', 'country']
    # This is used to link it to its manager class
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

    def is_staff(self):
        return self.staff