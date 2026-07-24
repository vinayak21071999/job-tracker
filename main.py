"""
Job tracker main entrypoint.

Run manually with:  python main.py
Deployed to run on a schedule via GitHub Actions (see .github/workflows/job_tracker.yml)
"""

import config
from matcher import filter_jobs
from notifier import notify_new_jobs
from scrapers.linkedin import fetch_all_linkedin_searches
from scrapers.workday import fetch_all_workday_companies
from seen_store import load_seen_ids, save_seen_ids


def collect_all_jobs():
    all_jobs = []

    all_jobs.extend(fetch_all_workday_companies(config.WORKDAY_COMPANIES))
    all_jobs.extend(fetch_all_linkedin_searches(config.LINKEDIN_SEARCHES))

    # Naukri (scrapers/naukri.py) is left in the repo but not called here -
    # its session cookie/nkparam expire too quickly (minutes, not days) to be
    # worth automating. Run it manually with fresh headers if you want an
    # occasional check: from scrapers.naukri import fetch_naukri_jobs

    return all_jobs


def main():
    print("Collecting jobs from all sources...")
    all_jobs = collect_all_jobs()
    print(f"Total postings collected: {len(all_jobs)}")

    matches = filter_jobs(all_jobs)
    print(f"Postings matching your profile: {len(matches)}")

    seen_ids = load_seen_ids()
    new_matches = [job for job in matches if job["id"] not in seen_ids]
    print(f"New matches not previously notified: {len(new_matches)}")

    if new_matches:
        notify_new_jobs(new_matches)
        seen_ids.update(job["id"] for job in new_matches)
        save_seen_ids(seen_ids)
    else:
        print("No new matches this run.")


if __name__ == "__main__":
    main()
