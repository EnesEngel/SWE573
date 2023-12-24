from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    cuisine =  models.ManyToManyField(Cuisine,blank=True)
    description = models.TextField(null=True)
    ingredients = models.JSONField(default=dict) 
    instructions = models.JSONField(default=dict)
    images = models.ImageField(null=True, blank=True, upload_to='images/')
    videos = models.URLField(null=True, blank=True)
    nutritionFacts = models.JSONField(null=True, blank=True) 
    preparationTime = models.PositiveIntegerField(null=True, blank=True)
    cookingTime = models.PositiveIntegerField(null=True, blank=True)  
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    averageRating = models.FloatField(default=0)
    class Meta:
        ordering = ['-updated','-created']

    def __str__(self):
        return self.title
    
    def calculateAverageRating(self):
        ratings = UserRating.objects.filter(recipe=self)
        total = 0

        if not ratings:
            self.averageRating = 0
        else:
            for rating in ratings:
                total += rating.value
                avg = total / ratings.count()
                self.averageRating = avg
            else:
                self.averageRating = 0

        self.save()


class UserBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)



class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[0:50]