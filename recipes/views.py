import logging
from django.http import JsonResponse
from .models import Unit, Unittype,Recipe, Category, UserComment, UserBookmark, Ingredient, Instruction
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RecipeForm, UserCommentForm
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.


logging.basicConfig(level=logging.DEBUG)

def add_comment(request, recipe_id):
    user_id = request.user.id
    user_instance = User.objects.get(pk=user_id)
    recipe_instance = Recipe.objects.get(pk=recipe_id)
    if request.method == 'POST':
        comment_form = UserCommentForm(request.POST)
        if comment_form.is_valid():
            print("Valid")
            new_comment = comment_form.save(commit=False)
            new_comment.user = user_instance
            new_comment.recipe = recipe_instance
            new_comment.save()
            return redirect('recipe', id=recipe_id)
        else:
            print(comment_form.errors)

def bookmark_toggle(request,recipe_id):
      try:
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        recipe_id = request.GET.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user_bookmark = UserBookmark.objects.filter(user=user, recipe=recipe)
        if user_bookmark.exists():
            user_bookmark.delete()
            return redirect('recipe', id=recipe_id)
        else:
            UserBookmark.objects.create(user=user, recipe=recipe)
            return redirect('recipe', id=recipe_id)
        
      except Exception as e:
        print(f"Error toggling bookmark: {e}")
        return redirect('recipe', id=recipe_id)

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

def sign_up_page(request):

    if request.method == "POST":

        
        form = UserCreationForm(request.POST)

        if not form.is_valid():
            
            messages.error(request, "Invalid signup form.")

        else:
            logging.debug("Signup form is valid. Saving the user.")

            user = form.save()
            login(request, user)

            return redirect('home')

    else:
        logging.debug("Creating a user signup form")
        form = UserCreationForm()

    return render(request, 'recipes/signup.html', {'form': form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''

    recipes=Recipe.objects.filter(
          Q(category__name__icontains=q) |
          Q(title__icontains=q) 
          )
    
    categorys=Category.objects.all()
    recipe_count=recipes.count()
    context={'recipes':recipes,'categorys':categorys,'recipe_count':recipe_count}
    return render(request,"recipes/home.html",context)

def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    comments =  UserComment.objects.filter(recipe=recipe)
    comment_form = UserCommentForm()

    is_bookmarked = UserBookmark.objects.filter(user=1, recipe=recipe).exists()

    if request.method == 'POST':
        if 'commentForm' in request.POST:
            add_comment(request, recipe.pk)
        elif 'addBookmarkForm' in request.POST:
            bookmark_toggle(request, recipe.pk)

    context = {'recipe': recipe, 'comments': comments, 'comment_form': comment_form, 'is_bookmarked':is_bookmarked}
    
    return render(request, 'recipes/recipe.html', context)

# def recipe(request,pk):
#         recipe=Recipe.objects.get(id=pk)
#         comments = UserComment.objects.filter(recipe=recipe)
#         comment_form = UserCommentForm()
#         if request.method == 'POST':
#             add_comment(request, recipe.pk)

#         context={'recipe':recipe,'comments': comments, 'comment_form': comment_form}
#         return render(request,"recipes/recipe.html",context)

@login_required(login_url='login')
def create_recipe(request):
    IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=('name', 'quantity'), extra=3)
    InstructionFormSet = inlineformset_factory(Recipe, Instruction, fields=('instruction_number', 'description'), extra=3)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST, instance=Recipe())
        instruction_formset = InstructionFormSet(request.POST, instance=Recipe())

        if recipe_form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
            recipe = recipe_form.save()
            ingredients = ingredient_formset.save(commit=False)
            for ingredient in ingredients:
                ingredient.recipe = recipe
                ingredient.save()

            instructions = instruction_formset.save(commit=False)
            for instruction in instructions:
                instruction.recipe = recipe
                instruction.save()

            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet(instance=Recipe())
        instruction_formset = InstructionFormSet(instance=Recipe())
        categories = Category.objects.all()    
    return render(request, 'recipes/recipe_form.html', {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset,
        'categories': categories,
    })

@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    

    if request.user != recipe.user:
       
        return redirect('recipe_detail', recipe_id=recipe_id)

    IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=('name', 'quantity'), extra=3)
    InstructionFormSet = inlineformset_factory(Recipe, Instruction, fields=('instruction_number', 'description'), extra=3)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
        instruction_formset = InstructionFormSet(request.POST, instance=recipe)

        if recipe_form.is_valid() and ingredient_formset.is_valid() and instruction_formset.is_valid():
            recipe = recipe_form.save()
            ingredient_formset.save()
            instruction_formset.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)
    else:
        recipe_form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe)
        instruction_formset = InstructionFormSet(instance=recipe)

    return render(request, 'recipes/update_recipe.html', {
        'recipe': recipe,
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset,
    })

@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    if request.user != recipe.user:
       
        return redirect('recipe_detail', recipe_id=recipe_id)

    if request.method == 'POST':
        recipe.delete()
        return redirect('home') 

    return render(request, 'recipes/confirm_delete_recipe.html', {'recipe': recipe})
@api_view(['GET'])
def GetUnitList(request):
    type = request.GET.get('type')
    return JsonResponse(list(Unit.objects.filter(type=request.GET.get('type')).values("id", "name")), safe=False)
@api_view(['GET'])
def GetUnitTypeList(request):
    return JsonResponse(list(Unittype.objects.all().values("id", "name")), safe=False)
@api_view(['GET'])
def GetCusineList(request):
      return JsonResponse(list(Category.objects.all().values("id", "name")), safe=False)

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