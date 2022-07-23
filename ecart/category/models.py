
from tabnanny import verbose
from unicodedata import category
from django.db import models
from django.urls import reverse

# Create your models here.

class MainCategory(models.Model):
    category_name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField( blank= True)
    cat_image = models.ImageField(upload_to='photos/categories', blank = True)

    class Meta:
        verbose_name = 'Main_category'
        verbose_name_plural='Main_categories' 

    def get_url(self):
            return reverse('product_by_main_category',args=[self.slug])
    def __str__(self):
        return self.category_name

class Category(models.Model):
    main_category = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description=models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name ='Category'
        verbose_name_plural='categories'
    
    def get_url(self):
            return reverse('product_by_category',args=[self.main_category.slug,self.slug])
    
    def __str__(self):
        return self.category_name

class Sub_Category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description=models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)

    class Meta:
        verbose_name ='sub_category'
        verbose_name_plural='sub_categories'
    
    def get_url(self):
            return reverse('product_by_sub_category',args=[self.category.main_category.slug,self.category.slug,self.slug])

    def __str__(self):
        return self.category_name