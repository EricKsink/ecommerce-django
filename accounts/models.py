from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')
        
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    
    #campos atributos django
    
    #Es la fecha que en la que se esta uniendo el usuario
    date_joined = models.DateTimeField(auto_now_add=True)
    
    #Es la fecha en la que el usuario se esta conectando por ultima vez
    last_login = models.DateTimeField(auto_now_add=True)
    
    #Es el campo que se utiliza para saber si el usuario es un administrador o no
    is_admin = models.BooleanField(default=False)
    
    #Es el campo que se utiliza para saber si es parte de la organizacion o no
    is_staff = models.BooleanField(default=False)
    
    #
    is_active = models.BooleanField(default=False)
    
    #Es superadmin?
    is_superadmin = models.BooleanField(default=False)
    
    
    #Es el campo que se utiliza para saber cual es el campo que se va a utilizar para iniciar sesion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = MyAccountManager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True