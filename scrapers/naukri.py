"""
Naukri scraper - NEEDS ONE-TIME SETUP FROM YOU.

Naukri's internal search API (https://www.naukri.com/jobapi/v3/search) requires
a header called "Nkparam" that's generated dynamically by their frontend JS and
rotates - unlike BigBasket, there's no fixed cookie/header set that keeps working.

To make this work, do the same thing you did for BigBasket:
1. Open https://www.naukri.com/qa-automation-engineer-jobs-in-bengaluru in Chrome
2. Open DevTools -> Network tab -> filter "Fetch/XHR"
3. Reload the page, find the request to "jobapi/v3/search"
4. Right-click it -> Copy -> Copy as cURL
5. Paste the headers you see (especially "nkparam", "appid", "systemid") below

Once you've done that, fill in FIXED_HEADERS and this module will work the same
way as the others. Until then, this module returns an empty list so the rest of
the pipeline still runs fine without it.
"""

import requests

SEARCH_URL = "https://www.naukri.com/jobapi/v3/search"

# TODO: paste the captured headers here after following the steps above
FIXED_HEADERS = {
    # "nkparam": "PASTE_CAPTURED_VALUE_HERE",
    # "appid": "PASTE_CAPTURED_VALUE_HERE",
    # "systemid": "Naukri",
    # "User-Agent": "Mozilla/5.0 ...",
}


def fetch_naukri_jobs(keyword: str, location: str = "", limit: int = 20):
    if "nkparam" not in FIXED_HEADERS:
        print("[naukri] skipped - FIXED_HEADERS not configured yet, see module docstring")
        return []

    params = {
        "noOfResults": limit,
        "urlType": "search_by_key_loc",
        "searchType": "adv",
        "keyword": keyword,
        "location": location,
    }
    try:
        resp = requests.get(SEARCH_URL, params=params, headers=FIXED_HEADERS, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[naukri] request failed: {e}")
        return []

    data = resp.json()
    jobs = []
    for item in data.get("jobDetails", []):
        jobs.append({
            "id": f"naukri:{item.get('jobId')}",
            "title": item.get("title", ""),
            "company": item.get("companyName", ""),
            "location": item.get("placeholders", {}).get("location", ""),
            "url": "https://www.naukri.com" + item.get("jdURL", ""),
        })
    return jobs
