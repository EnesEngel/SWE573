from django.forms import ModelForm
from .models import Recipe,UserComment
from django import forms
# from requests import get


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

class UserCommentForm(ModelForm):
    class Meta:
        model = UserComment
        fields = ['comment_text']        