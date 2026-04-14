from django.contrib import admin

from .models import CVItem, ItemPoint, Person, Recommender, Skill


class ItemPointInline(admin.TabularInline):
    model = ItemPoint
    extra = 1
    fields = ("text_is", "text_en")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city")
    search_fields = ("name", "email")
    fieldsets = (
        (None, {"fields": ("name", "kt")}),
        ("Contact", {"fields": ("email", "phone", "address", "city")}),
        ("Intro", {"fields": ("intro_is", "intro_en")}),
        ("Hobbies", {"fields": ("hobbies_is", "hobbies_en")}),
    )


@admin.register(CVItem)
class CVItemAdmin(admin.ModelAdmin):
    list_display = ("title_en", "item_type", "where_en", "start", "leave")
    list_filter = ("item_type",)
    search_fields = ("title_is", "title_en", "where_is", "where_en")
    date_hierarchy = "start"
    inlines = [ItemPointInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("skill_name_en", "skill_name_is", "skill_level")
    list_editable = ("skill_level",)
    search_fields = ("skill_name_is", "skill_name_en")


@admin.register(Recommender)
class RecommenderAdmin(admin.ModelAdmin):
    list_display = ("name", "workplace_en", "title_en", "email")
    search_fields = ("name", "workplace_en", "email")
