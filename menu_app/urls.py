from django.urls import path
from .views import menu, catalog, category

app_name = 'menu_app'

urlpatterns = [
    path('', catalog, name='catalog'),
  #  path('<slug:menu_slug>/', menu, name='menu'),
    path('<slug:category_slug>/', category, name='category'),
]
