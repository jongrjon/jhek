from django.urls import path

from . import views

app_name = "cv"

urlpatterns = [
    path("", views.cv_html, name="html"),
    path("pdf/", views.cv_pdf, name="pdf_default"),
    path("<str:lang>/", views.cv_html, name="html_lang"),
    path("pdf/<str:lang>/", views.cv_pdf, name="pdf"),
]
