from django.urls import path
from . import views

urlpatterns = [
    path("", views.Main.as_view()),
    path('item/<str:model>/', views.ItemView.as_view(), name='item_detail'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category_detail'),
]