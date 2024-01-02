from django.urls import path
from . import views 

urlpatterns=[
    path('signup/', views.sign_up_page, name='signup'),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path("",views.home,name="home"),
    path("recipe/<int:id>/",views.recipe,name="recipe"),
    
    path('create-recipe/',views.create_recipe,name="create-recipe"),
    path('update-recipe/<str:pk>/',views.update_recipe,name="update-recipe"),
    path('delete-recipe/<str:pk>/',views.delete_recipe,name="delete-recipe"),
    path('UnitTypeList/', views.GetUnitTypeList, name='UnitTypeList'),
    path('UnitList/', views.GetUnitList, name='UnitList'),
    path('UnitType/', views.GetUnitType, name='UnitType'),
    path('CusineList/', views.GetCusineList, name='CusineList'),

    path('add_comment/<int:recipe_id>', views.add_comment, name="add_comment"),
    path('bookmark_toggle/<int:recipe_id>', views.bookmark_toggle, name='bookmark_toggle'),

]