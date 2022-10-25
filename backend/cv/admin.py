from django.contrib import admin

# Register your models here

from cv.models import Person, CVItem, Skill, Reccommendor, ItemPoint

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person
    
@admin.register(CVItem)
class CVItemAdmin(admin.ModelAdmin):
    model = CVItem

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    model = Skill

@admin.register(Reccommendor)
class ReccommendorAdmin(admin.ModelAdmin):
    model = Reccommendor

@admin.register(ItemPoint)
class ItemPointAdmin(admin.ModelAdmin):
    model = ItemPoint

    
"""     list_display = (
        "id",
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    
    list_filter = (
        "published",
        "publish_date",
    )
    
    list_editable = (
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    
    search_fields =  (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    
    prepopulated_fields = {
        "slug" : (
            "title",
            "subtitle",
        )
    }
 
    date_hierarchy = "publish_date"
    save_on_top = True
"""
