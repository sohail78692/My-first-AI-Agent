import requests
import re
from html import unescape
from urllib.parse import urlparse


def fetch_webpage(url, max_characters=5000):
    """
    Fetch a webpage and extract readable text.
    """

    # ========================================================
    # 1. Validate URL
    # ========================================================

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ("http", "https"):
        return {
            "success": False,
            "url": url,
            "error": (
                "Invalid URL. Only HTTP and HTTPS "
                "are supported."
            )
        }


    # ========================================================
    # 2. Request webpage
    # ========================================================

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Encoding": "gzip, deflate, br"
    }


    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as error:

        return {
            "success": False,
            "url": url,
            "error": str(error)
        }


    # ========================================================
    # 3. Check content type
    # ========================================================

    content_type = response.headers.get(
        "Content-Type",
        ""
    )

    if "text/html" not in content_type.lower():

        return {
            "success": False,
            "url": url,
            "error": (
                "The URL did not return "
                "an HTML webpage."
            )
        }


    # ========================================================
    # 4. Get HTML
    # ========================================================

    html = response.text


    # ========================================================
    # 5. Remove scripts
    # ========================================================

    html = re.sub(
        r"<script\b[^>]*>.*?</script>",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )


    # ========================================================
    # 6. Remove styles
    # ========================================================

    html = re.sub(
        r"<style\b[^>]*>.*?</style>",
        " ",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )


    # ========================================================
    # 7. Remove comments
    # ========================================================

    html = re.sub(
        r"<!--.*?-->",
        " ",
        html,
        flags=re.DOTALL
    )


    # ========================================================
    # 8. Remove HTML tags
    # ========================================================

    text = re.sub(
        r"<[^>]+>",
        " ",
        html
    )


    # ========================================================
    # 9. Decode HTML entities
    # ========================================================

    text = unescape(text)


    # ========================================================
    # 10. Clean whitespace
    # ========================================================

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    # ========================================================
    # 11. Limit content
    # ========================================================

    if len(text) > max_characters:

        text = text[:max_characters]

        text += "\n...[content truncated]"


    # ========================================================
    # 12. Return result
    # ========================================================

    return {
        "success": True,
        "url": url,
        "content": text,
        "character_count": len(text)
    }