from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,PermissionsMixin)
from Branch.models import Branch

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,full_name='null',phone_number=None,branch=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),full_name=full_name,
                          phone_number=phone_number,branch=branch)
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_superuser(self, email, password):
        user = self.create_user(email,password=password,full_name="SITE CREATOR",)
        user.is_admin = True
        user.staff=True
        user.is_super_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    full_name =models.CharField(verbose_name='full name', max_length=255)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    phone_number = models.CharField("phone_number", max_length=20,null=True,blank=True)
    branch = models.ForeignKey(Branch, verbose_name="branch", related_name="branch", on_delete=models.SET_NULL,null=True)
    is_super_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    staff=models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        if not self.is_super_admin:
            if perm =="Users.add_user" or perm=="Users.change_user" or perm=="Users.delete_user":
                return False
            else:
                return True
        else:
            return True

    # remember to set appropriate permissions.
    def has_module_perms(self, app_label):
        if not self.is_super_admin:
            if app_label =="knox" or app_label=="auth" :
                return False
            else:
                return True
        else:
            return True
    @property

    def is_staff(self):
        return self.staff


class Customer(models.Model):
    """Model definition for Customer."""

    # TODO: Define fields here
    name = models.CharField(verbose_name='name', max_length=255)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    phone_number = models.CharField("phone_number", max_length=20,unique=True,)
    address = models.CharField(verbose_name="address", max_length=256)
    total_credit = models.IntegerField(verbose_name="total_credit",default=0)
    total_payment = models.IntegerField(verbose_name="total_payment",default=0)
    balance = models.IntegerField(verbose_name="total_balance",default=0)
    

    class Meta:
        """Meta definition for Customer."""

        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        """Unicode representation of Customer."""
        return f'{self.name} {self.phone_number}'
