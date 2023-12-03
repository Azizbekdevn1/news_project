from django.contrib.auth.models import AbstractUser,User
from django.db import models


# 1-way create Profile model
#class Profile(AbstractUser):
  #  photo=models.ImageField()
  #  birtdate=models.DateField()
   # address=models.TextField(blank=True)

#2-way create Profile model

class Profile(models.Model):
    objects = None
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='users_photos/',blank=True,null=True)
    birthdate=models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.user} profili"

