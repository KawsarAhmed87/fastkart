from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'status', 'slug')  # Fields to display in the list view
    search_fields = ('name', 'slug')  # Fields to include in the search
    prepopulated_fields = {'slug': ('name',)}  # Automatically populate slug from name
    list_filter = ('status',)  # Add filter for status

admin.site.register(Category, CategoryAdmin)
