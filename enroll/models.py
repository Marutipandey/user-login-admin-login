from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class MyDataModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    email = models.EmailField()


    def __str__(self):
        return self.name


from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ups_name = models.CharField(max_length=100)
    ups_serial_number = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=254)
    address = models.TextField()

    def __str__(self):
        return self.user.username
