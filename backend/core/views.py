from django.views.generic import TemplateView

from . import content


class HomeView(TemplateView):
    """Quiet domain landing page at /."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            tagline=content.TAGLINE,
            intro=content.INTRO,
            links=content.LINKS,
            contact_email=content.CONTACT_EMAIL,
        )
        return ctx
