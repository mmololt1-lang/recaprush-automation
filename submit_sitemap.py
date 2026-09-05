import requests
from urllib.parse import quote

import google.auth
from google.auth.transport.requests import Request


SITE_URL = "https://recaprush.blogspot.com/"
SITEMAP_URL = "https://recaprush.blogspot.com/sitemap.xml"

SCOPES = [
    "https://www.googleapis.com/auth/webmasters"
]


def get_credentials():
    credentials, project = google.auth.default(scopes=SCOPES)

    if not credentials.valid:
        credentials.refresh(Request())

    return credentials


def submit_sitemap():
    credentials = get_credentials()

    site_encoded = quote(SITE_URL, safe="")
    sitemap_encoded = quote(SITEMAP_URL, safe="")

    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{site_encoded}/sitemaps/{sitemap_encoded}"
    )

    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }

    response = requests.put(
        endpoint,
        headers=headers,
        timeout=30
    )

    if response.status_code in (200, 204):
        print("✅ RecapRush sitemap submitted successfully.")
        print(SITEMAP_URL)
    else:
        print("❌ Sitemap submission failed.")
        print("Status:", response.status_code)
        print(response.text)
        raise SystemExit(1)


if __name__ == "__main__":
    submit_sitemap()
