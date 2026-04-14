from django.contrib import admin

from .models import Post, Status, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "publish_date", "author")
    list_filter = ("status", "publish_date", "tags")
    search_fields = ("title", "subtitle", "slug", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_date"
    autocomplete_fields = ("tags",)
    save_on_top = True
    readonly_fields = ("date_created", "date_modified")

    fieldsets = (
        (None, {"fields": ("title", "subtitle", "slug", "author")}),
        ("Body", {"fields": ("body", "meta_description", "tags")}),
        (
            "Visibility",
            {
                "fields": ("status", "publish_date"),
                "description": (
                    "Draft = never served. Private = owner only. "
                    "Unlisted = by-slug only, noindex. Public = listed and indexable."
                ),
            },
        ),
        ("Metadata", {"fields": ("date_created", "date_modified")}),
    )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.setdefault("status", Status.DRAFT)
        initial.setdefault("author", request.user.pk)
        return initial
