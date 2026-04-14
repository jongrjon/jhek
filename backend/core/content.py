"""Editable homepage content. Edit and redeploy."""

TAGLINE = "Mostly email."

INTRO = "Occasional notes and links live here."

# All homepage links in one line. (label, url)
# Replace placeholder URLs with your actual profile URLs.
LINKS: list[tuple[str, str]] = [
    ("Notes", "/notes/"),
    ("GitHub", "https://github.com/jongrjon"),      # ← replace
    ("LinkedIn", "https://linkedin.com/in/jhek"),  # ← replace
]

# Set to an address to show the line; leave empty to hide.
CONTACT_EMAIL = ""
