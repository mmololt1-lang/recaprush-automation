import os
import json
import requests
from urllib.parse import quote
from google.oauth2 import service_account
from google.auth.transport.requests import Request

SITE_URL = "https://recaprush.blogspot.com/"
SITEMAP_URL = "https://recaprush.blogspot.com/sitemap.xml"

SCOPES = [
    "https://www.googleapis.com/auth/webmasters"
]

service_account_info = json.loads(
    os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
)

credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES
)


def get_access_token():
    if not credentials.valid:
        credentials.refresh(Request())

    return credentials.token


def submit_sitemap():
    token = get_access_token()

    site_encoded = quote(SITE_URL, safe="")
    sitemap_encoded = quote(SITEMAP_URL, safe="")

    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{site_encoded}/sitemaps/{sitemap_encoded}"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.put(
        endpoint,
        headers=headers,
        timeout=30
    )

    if response.status_code in (200, 204):
        print("✅ Sitemap Google Search Console руу амжилттай илгээгдлээ.")
        print(SITEMAP_URL)
    else:
        print("❌ Sitemap submit хийхэд алдаа гарлаа.")
        print("Status:", response.status_code)
        print(response.text)
        raise SystemExit(1)


if __name__ == "__main__":
    submit_sitemap()
