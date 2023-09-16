from django.contrib import admin

from app_category.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Class for displaying, creating and changing category in admin panel
    """

    list_display = ['id', 'title']
