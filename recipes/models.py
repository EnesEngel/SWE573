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

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True)
    images = models.ImageField(null=True, blank=True, upload_to='images/')
    videos = models.URLField(null=True, blank=True)
    nutritionFacts = models.JSONField(null=True, blank=True)
    preparationTime = models.PositiveIntegerField(null=True, blank=True)
    cookingTime = models.PositiveIntegerField(null=True, blank=True)
    averageRating = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

    def calculate_average_rating(self):
        ratings = UserRating.objects.filter(recipe=self)
        total = sum(rating.value for rating in ratings) if ratings else 0
        self.averageRating = total / ratings.count() if ratings else 0
        self.save()

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    instruction_number = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Instruction {self.instruction_number}: {self.description}"


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