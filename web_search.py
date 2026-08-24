import urllib.parse
import urllib.request
import re
from html import unescape


def clean_html(text):
    """Remove HTML tags and clean whitespace."""

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    text = unescape(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def web_search(query, max_results=5):
    """
    Search the web using DuckDuckGo HTML search.

    Returns:
        success
        query
        results containing:
            title
            url
            snippet
    """

    # ========================================================
    # 1. Build search URL
    # ========================================================

    encoded_query = urllib.parse.quote_plus(query)

    url = (
        "https://html.duckduckgo.com/html/"
        f"?q={encoded_query}"
    )


    # ========================================================
    # 2. Create HTTP request
    # ========================================================

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            )
        }
    )


    # ========================================================
    # 3. Send request
    # ========================================================

    try:

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            html = response.read().decode(
                "utf-8",
                errors="ignore"
            )

    except Exception as error:

        return {
            "success": False,
            "query": query,
            "results": [],
            "error": str(error)
        }


    # ========================================================
    # 4. Find search result blocks
    # ========================================================

    result_pattern = re.compile(
        r'<div[^>]+class="result[^"]*"[^>]*>'
        r'(.*?)'
        r'</div>\s*</div>',
        re.IGNORECASE | re.DOTALL
    )

    result_blocks = result_pattern.findall(html)


    # ========================================================
    # 5. Fallback: find result links directly
    # ========================================================

    if not result_blocks:

        result_blocks = re.findall(
            r'(<a[^>]+class="result__a"[^>]*>.*?</a>)',
            html,
            re.IGNORECASE | re.DOTALL
        )


    results = []


    # ========================================================
    # 6. Process result blocks
    # ========================================================

    for block in result_blocks:

        # ----------------------------------------------------
        # Extract URL
        # ----------------------------------------------------

        url_match = re.search(
            r'<a[^>]+class="result__a"[^>]+href="([^"]+)"',
            block,
            re.IGNORECASE | re.DOTALL
        )


        if not url_match:
            continue


        result_url = unescape(
            url_match.group(1)
        )


        # ----------------------------------------------------
        # Extract title
        # ----------------------------------------------------

        title_match = re.search(
            r'<a[^>]+class="result__a"[^>]*>'
            r'(.*?)'
            r'</a>',
            block,
            re.IGNORECASE | re.DOTALL
        )


        if not title_match:
            continue


        title = clean_html(
            title_match.group(1)
        )


        if not title:
            continue


        # ----------------------------------------------------
        # Clean DuckDuckGo redirect
        # ----------------------------------------------------

        if result_url.startswith("//"):

            result_url = "https:" + result_url


        parsed_url = urllib.parse.urlparse(
            result_url
        )

        query_params = urllib.parse.parse_qs(
            parsed_url.query
        )


        if "uddg" in query_params:

            result_url = query_params["uddg"][0]


        # ----------------------------------------------------
        # Ignore DuckDuckGo internal/ad URLs
        # ----------------------------------------------------

        parsed_result = urllib.parse.urlparse(
            result_url
        )

        hostname = parsed_result.hostname or ""


        if hostname.endswith(
            "duckduckgo.com"
        ):

            continue


        # ----------------------------------------------------
        # Validate URL
        # ----------------------------------------------------

        if not result_url.startswith(
            ("http://", "https://")
        ):

            continue


        # ----------------------------------------------------
        # Extract snippet
        # ----------------------------------------------------

        snippet_match = re.search(
            r'<a[^>]+class="result__snippet"[^>]*>'
            r'(.*?)'
            r'</a>',
            block,
            re.IGNORECASE | re.DOTALL
        )


        if not snippet_match:

            snippet_match = re.search(
                r'<div[^>]+class="result__snippet"[^>]*>'
                r'(.*?)'
                r'</div>',
                block,
                re.IGNORECASE | re.DOTALL
            )


        if snippet_match:

            snippet = clean_html(
                snippet_match.group(1)
            )

        else:

            snippet = ""


        # ----------------------------------------------------
        # Avoid duplicate URLs
        # ----------------------------------------------------

        if any(
            result["url"] == result_url
            for result in results
        ):

            continue


        # ----------------------------------------------------
        # Add result
        # ----------------------------------------------------

        results.append({
            "title": title,
            "url": result_url,
            "snippet": snippet
        })


        # ----------------------------------------------------
        # Stop at max results
        # ----------------------------------------------------

        if len(results) >= max_results:

            break


    # ========================================================
    # 7. Return results
    # ========================================================

    return {
        "success": True,
        "query": query,
        "results": results
    }