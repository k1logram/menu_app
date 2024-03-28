from django.contrib import admin
from menu_app.models import Categories, Menus


@admin.register(Menus)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']
    search_fields = ['name']
    fields = [
        'name',
        'slug'
    ]


@admin.register(Categories)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', 'menu', 'parent_category']
    search_fields = ['name']
    fields = [
        'name',
        'slug',
        'menu',
        'parent_category'
    ]
