"""Project URL configuration.

Route layout:
    /           core (homepage)
    /notes/     notes (blog app)
    /cv/        CV (HTML + PDF), private by default
    /admin/     Django admin — primary editing interface
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("notes/", include("blog.urls")),
    path("cv/", include("cv.urls")),
]
