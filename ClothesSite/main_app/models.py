from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

'''
Site model is an extension of the django User object
django User object has the following fields:
username, password, email, first_name, last_name.
'''

def get_image_path(instance, filename):
    return '/'.join(['clothes_images', str(instance.name), filename])


class Clothes_Item(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=32, default="N/A")
    size = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=32, default="N/A")
    image = models.ImageField(upload_to='clothes_images', default='media/default.png')
    gender = models.CharField(max_length=14)
    #clothing_choices represents all possible choices for any gender, so that the form validates correctly in the view
    clothing_choices = [('Tops', 'Tops'), ('Bottoms', 'Bottoms'), ('Dresses', 'Dresses'), ('Shoes', 'Shoes'),('Accessories', 'Accessories'), ('Costumes', 'Costumes'), ('Other', 'Other')]
    clothing_type = models.CharField(choices=clothing_choices, max_length=14)

    def __str__(self):
        return self.name

'''
SORT FILTERS
gender              (male, female, unisex)
price               input own price filter
clothing_type       from given options

'''


class Favorite(models.Model):
    user = models.ForeignKey(User)
    clothes_item = models.ForeignKey(Clothes_Item)

    #add __str__(self): implementation

