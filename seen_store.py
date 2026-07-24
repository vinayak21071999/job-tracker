"""
Keeps track of job IDs we've already notified about, stored as a JSON file.
In GitHub Actions, this file is committed back to the repo after each run
so state persists between scheduled runs.
"""

import json
import os

import config


def load_seen_ids() -> set:
    if not os.path.exists(config.SEEN_JOBS_FILE):
        return set()
    with open(config.SEEN_JOBS_FILE, "r") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()


def save_seen_ids(seen_ids: set):
    with open(config.SEEN_JOBS_FILE, "w") as f:
        json.dump(sorted(seen_ids), f, indent=2)
