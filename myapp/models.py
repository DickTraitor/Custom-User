from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,AbstractUser
)
class User(AbstractUser):
    pass

class MyUserManager(BaseUserManager):
    def create_user(self, account_number, date_of_birth, password=None):
        """
        Creates and saves a User with the given account_number, date of
        birth and password.
        """
        if not account_number:
            raise ValueError('Users must have an account_number!')

        user = self.model(
            account_number=account_number,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account_number, date_of_birth, password):
        """
        Creates and saves a superuser with the given account_number, date of
        birth and password.
        """
        user = self.create_user(
            account_number,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    account_number = models.IntegerField(unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'account_number'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.account_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin