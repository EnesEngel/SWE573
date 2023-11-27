from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Recipe, Cuisine
from .forms import RecipeForm
# Create your views here.


def loginPage(request):

      if request.user.is_authenticated:
            return redirect('home')
      if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            try:
                  user=User.objects.get(username=username)
            except:
                  messages.error(request,'User does not exist.')
            user= authenticate(request,username=username,password=password)

            if user is not None:
                  login(request,user)
                  return redirect('home')
            else:
                  messages.error(request,'Username OR Password does not exist.')

      context={}
      return render(request,'recipes/login_register.html',context)

def logoutUser(request):
      logout(request)
      return redirect('home')

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''

    recipes=Recipe.objects.filter(
          Q(cuisine__name__icontains=q) |
          Q(title__icontains=q) |
          Q(instructions__icontains=q) 
          )
    
    cuisines=Cuisine.objects.all()
    recipe_count=recipes.count()
    context={'recipes':recipes,'cuisines':cuisines,'recipe_count':recipe_count}
    return render(request,"recipes/home.html",context)


def recipe(request,pk):
        recipe=Recipe.objects.get(id=pk)
        context={'recipe':recipe}
        return render(request,"recipes/recipe.html",context)

@login_required(login_url='login')
def createRecipe(request):
      form = RecipeForm()
      if request.method== 'POST':
            form= RecipeForm(request.POST)
            if form.is_valid():
                  form.save()
                  return redirect('home')
                
      context = {'form' : form}
      return render(request,'recipes/recipe_form.html', context)

@login_required(login_url='login')
def updateRecipe(request,pk):
      recipe=Recipe.objects.get(id=pk)
      form=RecipeForm(instance=recipe)
      
      if request.user != recipe.owner:
            return HttpResponse('You are not allowed here!!')
      if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
                  form.save()
                  return redirect('home')
      context={'form':form}
      return render(request,'recipes/recipe_form.html',context)

@login_required(login_url='login')
def deleteRecipe(request,pk):
      recipe=Recipe.objects.get(id=pk)
       
      if request.user != recipe.owner:
            return HttpResponse('You are not allowed here!!')
      if request.method=='POST':
            recipe.delete()
            return redirect('home')
      return render(request,'recipes/delete.html',{'obj':recipe})
