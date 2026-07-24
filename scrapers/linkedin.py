"""
Scraper for LinkedIn's public "guest" job search endpoint.
This is the same endpoint LinkedIn's own site calls for infinite-scroll job
results, and it works without logging in. It returns an HTML fragment (not
JSON) that we parse with BeautifulSoup.

Note: LinkedIn will throttle/block after a handful of requests from the same
IP in a short window. Keep max_pages small and add delays if you expand this.
"""

import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
}


def fetch_linkedin_jobs(keywords: str, location: str, max_pages: int = 2, delay_seconds: float = 2.0):
    """
    Returns a list of dicts: {id, title, company, location, url}
    Each page returns up to 25 postings.
    """
    jobs = []

    for page in range(max_pages):
        start = page * 25
        params = {
            "keywords": keywords,
            "location": location,
            "start": start,
        }
        url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[linkedin] request failed: {e}")
            break

        if not resp.text.strip():
            break  # no more results

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("li")
        if not cards:
            break

        for card in cards:
            link_tag = card.find("a", class_="base-card__full-link")
            title_tag = card.find("h3", class_="base-search-card__title")
            company_tag = card.find("h4", class_="base-search-card__subtitle")
            location_tag = card.find("span", class_="job-search-card__location")

            if not link_tag:
                continue

            job_url = link_tag.get("href", "").split("?")[0]
            job_id = job_url.rstrip("/").split("-")[-1]  # LinkedIn job ID is the trailing number

            jobs.append({
                "id": f"linkedin:{job_id}",
                "title": title_tag.get_text(strip=True) if title_tag else "",
                "company": company_tag.get_text(strip=True) if company_tag else "",
                "location": location_tag.get_text(strip=True) if location_tag else "",
                "url": job_url,
            })

        time.sleep(delay_seconds)

    return jobs


def fetch_all_linkedin_searches(searches):
    """searches: list of {"keywords", "location"} dicts from config.py"""
    all_jobs = []
    for search in searches:
        jobs = fetch_linkedin_jobs(search["keywords"], search["location"])
        print(f"[linkedin] '{search['keywords']}' in '{search['location']}': {len(jobs)} postings")
        all_jobs.extend(jobs)
    return all_jobs
