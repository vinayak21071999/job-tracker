"""
Generic scraper for any company that uses Workday for its careers site.

Workday exposes a JSON search API at:
    https://{tenant}.wd{n}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs

No auth needed - it's the same endpoint the public careers page itself calls.
"""

import requests

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}


def fetch_workday_jobs(tenant: str, wd: int, site: str, search_text: str = "", limit: int = 20, max_pages: int = 5):
    """
    Fetch job postings from a Workday-based careers site.

    Returns a list of dicts: {id, title, location, posted_on, url}
    """
    base_url = f"https://{tenant}.wd{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
    careers_base = f"https://{tenant}.wd{wd}.myworkdayjobs.com/{site}"

    jobs = []
    offset = 0

    for _ in range(max_pages):
        payload = {
            "appliedFacets": {},
            "limit": limit,
            "offset": offset,
            "searchText": search_text,
        }
        try:
            resp = requests.post(base_url, json=payload, headers=HEADERS, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[workday:{tenant}] request failed: {e}")
            break

        data = resp.json()
        postings = data.get("jobPostings", [])
        if not postings:
            break

        for posting in postings:
            path = posting.get("externalPath", "")
            jobs.append({
                "id": f"workday:{tenant}:{path}",
                "title": posting.get("title", ""),
                "location": posting.get("locationsText", ""),
                "posted_on": posting.get("postedOn", ""),
                "url": careers_base + path,
            })

        total = data.get("total", 0)
        offset += limit
        if offset >= total:
            break

    return jobs


def fetch_all_workday_companies(companies, search_text: str = ""):
    """companies: list of {"name", "tenant", "wd", "site"} dicts from config.py"""
    all_jobs = []
    for company in companies:
        jobs = fetch_workday_jobs(
            tenant=company["tenant"],
            wd=company["wd"],
            site=company["site"],
            search_text=search_text,
        )
        for job in jobs:
            job["company"] = company["name"]
        print(f"[workday:{company['name']}] found {len(jobs)} postings")
        all_jobs.extend(jobs)
    return all_jobs
