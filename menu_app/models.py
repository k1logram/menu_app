from django.db import models


class Menus(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True, verbose_name='url')

    class Meta:
        db_table = 'menu'
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    menu = models.ForeignKey(to=Menus, on_delete=models.CASCADE, verbose_name='Меню')
    parent_category = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родительская категория')
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True, verbose_name='url')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
