from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.core.validators import RegexValidator
import random, datetime
from django.utils import timezone


BANK, CASH = ('karta', 'naxt')

class CustomUser(AbstractUser):

    PAYMENT_TYPE = (
        (BANK, 'karta'),
        (CASH, 'naxt')
    )

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    username = None
    phone_number = models.CharField(max_length=15, unique=True, validators=[
        RegexValidator(regex=r'^\+998\d{9}$', message="Telefon raqam noto'g'ri formatda")])
    address = models.TextField()
    payment = models.CharField(max_length=10, choices=PAYMENT_TYPE)
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'


    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",
        blank=True
    )


    def __str__(self):
        return self.first_name


    def generate_verify_code(self):
        code = ''.join(str(random.randint(0, 9)) for _ in range(5))
        UserConfirmation.objects.create(
            user = self,
            code = code,
            expires = timezone.now() + datetime.timedelta(minutes=2)
        )

        return code
    

class UserConfirmation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otp_code')
    code = models.CharField(max_length=5)
    expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.code}'