from django.contrib import admin
from .models import Brand, Category, ProductTypeOne, ProductTypeTwo, ProductTypeThree

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductTypeOne)
admin.site.register(ProductTypeTwo)
admin.site.register(ProductTypeThree)
