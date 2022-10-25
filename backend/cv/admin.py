from django.contrib import admin

# Register your models here

from cv.models import Person, CVItem, Skill, Reccommendor, ItemPoint

class PointInline(admin.TabularInline):
    model = ItemPoint

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person

@admin.register(CVItem)
class CVItemAdmin(admin.ModelAdmin):
    model = CVItem
    inlines = [
        PointInline,
    ]

@admin.register(Skill)
class killAdmin(admin.ModelAdmin):
    model = Skill

@admin.register(Reccommendor)
class RecommendorAdmin(admin.ModelAdmin):
    model = Reccommendor

@admin.register(ItemPoint)
class ItemPointAdmin(admin.ModelAdmin):
    model = ItemPoint


    