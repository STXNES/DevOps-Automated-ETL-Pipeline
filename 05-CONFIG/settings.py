import os
from pathlib import Path

# ============================================
# PROJECT ROOT
# ============================================
ROOT = Path(__file__).resolve().parents[1]

# ============================================
# FILES
# ============================================
PIPELINE_FOLDER = ROOT / "01-PIPELINE"
MASTER_DATABASE = ROOT / "02-MASTER_DATABASE" / "master_database.csv"
LOG_FILE = ROOT / "05-LOGS" / "send_log.txt"

# ============================================
# GMAIL / SMTP API
# ============================================
CREDENTIALS = ROOT / "05-CONFIG" / "credentials.json"
TOKEN = ROOT / "05-CONFIG" / "token.json"

# ============================================
# OUTREACH SETTINGS
# ============================================
DELAY_SECONDS = int(os.environ.get("DELAY_SECONDS", 60))
SUBJECT = os.environ.get("EMAIL_SUBJECT", "Automated DevOps & Data Integration Workflow")
