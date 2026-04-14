"""CV views — private-first.

Both HTML and PDF renderings are @login_required. The CV contains PII
(kennitala, phone, address); do not expose without authentication.
"""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from .models import CVItem, ItemType, Person, Recommender, Skill

SUPPORTED_LANGS = ("is", "en")


def _resolve_lang(request, lang_arg: str | None) -> str:
    lang = lang_arg or request.GET.get("lang") or getattr(
        settings, "CV_DEFAULT_LANGUAGE", "is"
    )
    return lang if lang in SUPPORTED_LANGS else "is"


def _build_context(lang: str) -> dict[str, Any]:
    """Collect all CV data, grouped by section, language-aware.

    Returns a dict the template can iterate over without re-doing data shaping.
    """
    person = Person.objects.first()
    items = list(CVItem.objects.prefetch_related("points").all())

    def section(type_code: str) -> list[CVItem]:
        return [i for i in items if i.item_type == type_code]

    skills = list(Skill.objects.all())

    return {
        "lang": lang,
        "is_is": lang == "is",
        "person": person,
        "jobs": section(ItemType.JOB),
        "education": section(ItemType.EDUCATION),
        "seminars": section(ItemType.SEMINAR),
        "skills": skills,
        "recommenders": Recommender.objects.all(),
    }


@login_required
def cv_html(request, lang: str | None = None):
    ctx = _build_context(_resolve_lang(request, lang))
    ctx["pdf_url"] = reverse("cv:pdf", kwargs={"lang": ctx["lang"]})
    return render(request, "cv/cv.html", ctx)


@login_required
def cv_pdf(request, lang: str | None = None):
    try:
        from weasyprint import HTML
    except ImportError as exc:  # pragma: no cover - env-dependent
        return HttpResponse(
            f"PDF rendering unavailable: {exc}. Install WeasyPrint and its "
            "system dependencies (libpango, libcairo, libgdk-pixbuf).",
            status=503,
            content_type="text/plain; charset=utf-8",
        )

    ctx = _build_context(_resolve_lang(request, lang))
    html_string = render_to_string("cv/cv_pdf.html", ctx, request=request)
    pdf_bytes = HTML(
        string=html_string, base_url=request.build_absolute_uri("/")
    ).write_pdf()

    filename = f"jhek-cv-{ctx['lang']}.pdf"
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
