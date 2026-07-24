"""
Central configuration for the job tracker.
Edit this file to tune what counts as a match.
"""

# --- Target roles (job title should contain at least one of these, case-insensitive) ---
TARGET_TITLES = [
    "qa automation engineer",
    "software test engineer",
    "python automation engineer",
    "sdet",
    "automation test engineer",
    "manual test engineer",
    "test engineer",          # broader catch-all, still filtered by keywords below
    "qa engineer",
]

# --- Skill / domain keywords (used to score relevance, esp. for broad titles) ---
SKILL_KEYWORDS = [
    "python", "selenium", "pytest", "api testing", "postman", "sql", "git",
    "automation testing", "manual testing", "medical device testing",
    "polarion", "jira", "dicom", "pacs",
    # related keywords worth catching too
    "test automation", "regression testing", "test case", "test plan",
    "robot framework", "junit", "testng", "rest assured", "appium",
    "iec 62304", "fda 21 cfr", "iso 13485", "hl7", "quality management system",
    "defect tracking", "bug tracking", "test strategy", "black box testing",
    "white box testing", "load testing", "performance testing", "ci/cd",
    "jenkins", "azure devops", "test rail",
]

# --- Preferred locations (job location should contain at least one of these) ---
TARGET_LOCATIONS = [
    "bengaluru", "bangalore", "mysore", "mysuru", "pune", "remote", "india",
]

# Minimum years of experience mentioned in the posting that you'd still consider
# (used only as a soft filter where the source exposes an experience field)
MIN_EXPERIENCE_YEARS = 0   # keep 0 to not filter by experience; postings rarely state it cleanly
MAX_EXPERIENCE_YEARS = 12

# --- Companies on Workday: (display_name, tenant, wd_number, site) ---
# URL pattern: https://{tenant}.wd{wd_number}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs
WORKDAY_COMPANIES = [
    {"name": "Philips", "tenant": "philips", "wd": 3, "site": "jobs-and-careers"},
    {"name": "Siemens Healthineers", "tenant": "onehealthineers", "wd": 3, "site": "SHSJB"},
    {"name": "GE HealthCare", "tenant": "gehc", "wd": 5, "site": "GEHC_ExternalSite"},
    # Add more Workday-based companies here as you confirm their tenant/site, e.g.:
    # {"name": "Dell", "tenant": "dell", "wd": 1, "site": "External"},
    # {"name": "Cisco", "tenant": "cisco", "wd": 5, "site": "External"},
]

# --- LinkedIn guest search queries to run (keyword + location pairs) ---
LINKEDIN_SEARCHES = [
    {"keywords": "QA Automation Engineer", "location": "Bengaluru, Karnataka, India"},
    {"keywords": "SDET", "location": "India"},
    {"keywords": "Automation Test Engineer", "location": "Pune, Maharashtra, India"},
    {"keywords": "Python Automation Engineer", "location": "India"},
]

# --- Telegram ---
# Set these as GitHub Actions secrets: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
# (same bot you already set up for the Hot Wheels tracker can be reused, or make a new one)

# --- File that stores job IDs we've already notified about, so we don't repeat ---
SEEN_JOBS_FILE = "seen_jobs.json"
