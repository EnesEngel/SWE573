from django.http import JsonResponse
from .models import Unit, Unittype,Recipe, Cuisine
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RecipeForm
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
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
      return render(request,'recipes/recipe_formAlt.html', context)

@login_required(login_url='login')
def updateRecipe(request,pk):
      recipe=Recipe.objects.get(id=pk)
      form=RecipeForm(instance=recipe)
      
      if request.user != recipe.user:
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
       
      if request.user != recipe.user:
            return HttpResponse('You are not allowed here!!')
      if request.method=='POST':
            recipe.delete()
            return redirect('home')
      return render(request,'recipes/delete.html',{'obj':recipe})


@api_view(['GET'])
def GetUnitList(request):
    type = request.GET.get('type')
    return JsonResponse(list(Unit.objects.filter(type=request.GET.get('type')).values("id", "name")), safe=False)
@api_view(['GET'])
def GetUnitTypeList(request):
    return JsonResponse(list(Unittype.objects.all().values("id", "name")), safe=False)
@api_view(['GET'])
def GetCusineList(request):
      return JsonResponse(list(Cuisine.objects.all().values("id", "name")), safe=False)


@api_view(['POST'])
def CreateBlog(request):
    _blog = blog.objects.create(category_id=request.data.get('category'), title=request.data.get('title'),slug=request.data.get('slug'),excerpt=request.data.get('excerpt'),
    content=request.data.get('content'),contentTwo=request.data.get('contentTwo'),image=request.data.get('image'),ingredients=request.data.get('ingredients'),postlabel=request.data.get('postlabel'))
    return JsonResponse(_blog.id, safe=False)

@api_view(['POST']) 
def File(request):
    file = request.FILES['file']
    file_name = default_storage.save('image\\' + file.name, file)
    return JsonResponse(file_name, safe=False)

@api_view(['GET'])
def GetUnitType(request):
    return JsonResponse(model_to_dict(Unittype.objects.get(id=request.GET.get('id'))), safe=False)