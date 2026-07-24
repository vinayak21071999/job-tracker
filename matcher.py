"""
Decides whether a scraped job posting is relevant to your profile.
"""

import config


def is_title_match(title: str) -> bool:
    title_lower = title.lower()
    return any(t in title_lower for t in config.TARGET_TITLES)


def is_location_match(location: str) -> bool:
    if not location:
        return True  # don't reject jobs where location wasn't captured (e.g. some Workday postings)
    location_lower = location.lower()
    return any(loc in location_lower for loc in config.TARGET_LOCATIONS)


def matched_skills(text: str):
    text_lower = text.lower()
    return [kw for kw in config.SKILL_KEYWORDS if kw in text_lower]


def filter_jobs(jobs):
    """
    jobs: list of dicts with at least "title" and "location" keys.
    Returns only the jobs worth notifying about.
    """
    matches = []
    for job in jobs:
        title = job.get("title", "")
        location = job.get("location", "")

        if not is_title_match(title):
            continue
        if not is_location_match(location):
            continue

        job["matched_skills"] = matched_skills(title)
        matches.append(job)

    return matches
