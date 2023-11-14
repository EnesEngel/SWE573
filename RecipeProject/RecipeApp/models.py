from django.db import models

# Create your models here.

class Users(models.Model):
    UserId=models.AutoField(primary_key=True)
    UserName= models.CharField(max_length=100)


class Recipes(models.Model):
    RecipeId=models.AutoField(primary_key=True)
    RecipeTitle= models.CharField(max_length=100)
    RecipeDate= models.DateField()
    PhotoFilePath= models.CharField(max_length=100)
    RecipeTitle= models.CharField(max_length=100)
