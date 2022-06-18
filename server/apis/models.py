from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, fullName=None,verified=False,photo=None,phone=None,address=None,balance=0,uid=uuid.uuid4(),isUser=False,isDeliveryGuy=False,isSeller=False, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fullName=fullName,
            verified=verified,
            photo=photo,
            phone=phone,
            address=address,
            balance=balance,
            uid=uid,
            isUser=isUser,
            isDeliveryGuy=isDeliveryGuy,
            isSeller=isSeller

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullName=None,verified=False,photo=None,phone=None,address=None, balance=0,uid=uuid.uuid4(),isUser=False,isDeliveryGuy=False,isSeller=False,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            fullName=fullName,
            verified=verified,
            photo=photo,
            phone=phone,
            address=address,
            balance=balance,
            uid=uid,
            isUser=isUser,
            isDeliveryGuy=isDeliveryGuy,
            isSeller=isSeller
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    fullName=models.CharField(max_length=300)
    verified=models.BooleanField(default=False)
    photo=models.ImageField(upload_to='uploads/',blank=True)
    phone=models.CharField(max_length=10,unique=True)
    address=models.CharField(max_length=2000)
    balance=models.IntegerField(default=0)
    uid=models.CharField(max_length=3000,default=uuid.uuid4())
    isUser=models.BooleanField(default=False)
    isDeliveryGuy=models.BooleanField(default=False)
    isSeller=models.BooleanField(default=False)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullName','phone','address']

    def __str__(self):
        return self.email

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

# Product
class Product(models.Model):
    productName=models.CharField(max_length=300)
    description=models.TextField(max_length=3000)
    productPrice=models.IntegerField()
    quantity=models.IntegerField(default=0)
    photo=models.ImageField(upload_to='uploads/',blank=True)
    postedby=models.ForeignKey(User,on_delete=models.CASCADE,related_name='postedby')

    def __str__(self):
        return self.productName