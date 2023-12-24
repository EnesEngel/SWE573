from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Unit(models.Model):
    name = models.CharField(max_length=255)
    unittype =models.IntegerField()

    def __str__(self):
        return self.name
    
class Unittype(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 

class Cuisine(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Recipe(models.Model):
    owner = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    cuisine =  models.ForeignKey(Cuisine,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    instructions= models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.title




class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[0:50]