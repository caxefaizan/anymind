from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):

    email = models.EmailField(blank = False, max_length=100, verbose_name='email')
    clock_active = models.BooleanField(blank= True, default=False)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

class Clock(models.Model):
    current_date = models.DateField()
    clockedIn = models.DateTimeField(blank = True, null=True)
    clockedOut = models.DateTimeField(blank = True, null=True)
    totalHours = models.IntegerField(blank = True, default=0)
    user = models.ForeignKey(
        MyUser, related_name="User", on_delete=models.CASCADE
    )
    def __str__(self):
        return self.current_date.strftime("%d %b %Y ")