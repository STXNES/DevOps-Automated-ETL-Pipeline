# DevOps Automated ETL & Outreach Pipeline

<p align="center">
  <img src="https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Runtime-Python_3.10-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10" />
  <img src="https://img.shields.io/badge/Telemetry-Streamlit_Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL_%2F_Neon-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Protocols-DNS_Sec_(SPF%2FDKIM%2FDMARC)-00C2FF?style=for-the-badge&logo=cloudflare&logoColor=white" alt="DNS Security" />
</p>

An enterprise-grade, **serverless ETL (Extract, Transform, Load) and automated data pipeline** built with **GitHub Actions CI/CD**, Python, and Streamlit. The system executes automated scheduled web extraction, performs programmatic **DNS mail-health audits (MX, SPF, DKIM, DMARC)**, sanitizes and deduplicates high-volume datasets, feeds an operational telemetry dashboard, and synchronizes data into a serverless PostgreSQL database in the cloud.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    subgraph Scheduling ["⏰ CI/CD Trigger Layer"]
        A["Cron Schedule (0 15 * * *)"] --> B["GitHub Actions Runner (Ubuntu)"]
        A2["Manual workflow_dispatch"] --> B
    end

    subgraph Ingestion ["🔍 Data Ingestion & Extraction"]
        B --> C["Headless Web Scraper (DuckDuckGo Engine)"]
        C --> D["Raw Target Payloads (altus_prospects.csv)"]
    end

    subgraph Transformation ["🛡️ Transformation & Quality Assurance"]
        D --> E["Data Sanitizer (clean_csv.py)"]
        E --> F1["Regex RFC Email Validation"]
        E --> F2["URL Canonicalization"]
        E --> F3["DNS MX Record Verification (dnspython)"]
        F3 --> G["Master DB Reconciliation (Deduplication)"]
    end

    subgraph Security ["🔒 Network Security & Deliverability"]
        G --> H["DNS Mail Security Audit (SPF / DKIM / DMARC)"]
        H --> I["Automated Multi-Stage Follow-ups (IMAP / SMTP)"]
    end

    subgraph Storage ["📊 Storage, Analytics & Cloud Sync"]
        G --> J["Partitioned Pipeline Batches (01-PIPELINE/Batch_*.csv)"]
        G --> K["Master Database CSV (Append-Only)"]
        K --> L["Streamlit Command Center (app.py)"]
        K --> M["Vercel Postgres / Neon DB Sync (migrate.js)"]
    end
```

---

## ⚡ Core Technical Capabilities

### 1. 🔄 Serverless CI/CD Automation (GitHub Actions)
* **Automated Autopilot:** Runs on a scheduled POSIX cron schedule (`0 15 * * *`) on ephemeral Ubuntu virtual environments without requiring a dedicated persistent server.
* **Secure Credential Injection:** Secrets (`ZOHO_EMAIL`, `DATABASE_URL`, `GEMINI_API_KEY`) are dynamically injected in-memory at runtime and scrubbed immediately after execution (`rm -f 05-CONFIG/email_credentials.json`).
* **Automated State Persistence:** Processed lead batches and master dataset updates are automatically committed and pushed back to the repository by `github-actions[bot]` with `[skip ci]` flags to prevent recursive triggering.

### 2. 🌐 Network Protocol & Mail Deliverability Auditing
* **Programmatic MX Verification:** Validates target domain mail exchange (MX) records in real-time using `dnspython` prior to pipeline insertion, discarding dead domains and protecting reputation.
* **SPF / DKIM / DMARC Audit Suite (`check_domain_health.py`):**
  * **SPF (`v=spf1`):** Resolves TXT authorization records to ensure originating IPs are permitted senders.
  * **DKIM (`zmail._domainkey`):** Queries cryptographic public key selector records for message signing integrity.
  * **DMARC (`_dmarc`):** Evaluates domain alignment and reporting policy (`p=none`/`p=reject`) to eliminate spoofing vulnerabilities and spam classification.

### 3. 🧹 Heuristic Data Sanitization & Deduplication (`clean_csv.py`)
* **Strict Heuristic Filters:** Strips out image-based crawler traps (`.png`, `.svg`, `.webp`), placeholder domains, and generic notification addresses (`noreply`, `sentry`, `cloudflare`).
* **Batching & Partitioning:** Splits incoming pipelines into discrete batches (`Batch_001.csv`, `Batch_002.csv`) to respect API rate limits and avoid throttling.
* **Reconciliation Engine:** Matches prospective records against a centralized, append-only master database to ensure complete duplicate prevention across subsequent extraction runs.

### 4. 📈 Operations Command Center & Telemetry (Streamlit)
* **Executive Analytics Dashboard (`03-SCRIPTS/Dashboard/app.py`):**
  * Custom dark-themed user interface styled with custom CSS (`#0E1116` / `#161A21`).
  * Real-time funnel metrics: total prospects ingested, validated leads, active batches, and delivery status.
  * Geographic breakdown: interactive lead filtering by City, State, and Country.

### 5. ☁️ Cloud Database Migration (PostgreSQL / Neon)
* **Node.js Sync Bridge (`crm-app/migrate.js`):** Automatically maps and migrates sanitized master CSV data to serverless PostgreSQL (`Neon` / `Vercel Postgres`), bridging flat-file batch storage with relational relational query workloads.

---

## 📂 Repository Structure

```text
├── .github/
│   └── workflows/
│       └── daily_outreach.yml       # GitHub Actions CI/CD Cron Autopilot
├── 01-PIPELINE/                     # Partitioned data batches (Batch_001.csv, ...)
├── 02-MASTER_DATABASE/              # Centralized append-only master dataset
├── 03-SCRIPTS/
│   ├── Cleaner/
│   │   └── clean_csv.py             # Data sanitization, regex & batch partitioning
│   ├── Dashboard/
│   │   └── app.py                   # Streamlit Telemetry Command Center
│   ├── Email/
│   │   ├── check_domain_health.py   # DNS resolver (SPF, DKIM, DMARC auditor)
│   │   ├── auto_followup.py         # Multi-stage automated follow-up engine
│   │   └── send_pipeline.py         # Delivery pipeline with LLM personalization
│   ├── Gmail_API/
│   │   └── read_replies.py          # IMAP bounce and reply listener
│   └── Scraper/
│       └── auto_scraper.py          # Headless web extraction engine
├── crm-app/                         # Next.js Client Interface & DB migration scripts
│   └── migrate.js                   # CSV-to-PostgreSQL (Neon) migration bridge
├── .env.example                     # Environment template for local runs
├── requirements.txt                 # Python dependencies
└── README.md                        # Technical documentation
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/STXNES/devops-automated-etl-pipeline.git
cd devops-automated-etl-pipeline

python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your secrets:
```bash
cp .env.example .env
```

### 3. Run DNS Mail Security Audit
```bash
python 03-SCRIPTS/Email/check_domain_health.py
```

### 4. Launch the Streamlit Analytics Dashboard
```bash
streamlit run 03-SCRIPTS/Dashboard/app.py
```

---

## 🔐 GitHub Actions Secrets Reference

| Secret Name | Purpose | Example / Format |
| :--- | :--- | :--- |
| `ZOHO_EMAIL` | Originating authenticated SMTP address | `outreach@domain.com` |
| `ZOHO_APP_PASSWORD` | App-specific password for SMTP authentication | `xxxx-xxxx-xxxx-xxxx` |
| `DATABASE_URL` | Cloud PostgreSQL connection string | `postgresql://user:pass@ep-...neon.tech/neondb` |
| `GEMINI_API_KEY` | Google Gemini API key for dynamic icebreakers | `AIzaSy...` |
| `GROK_API_KEY` | xAI Grok API key for natural language processing | `xai-...` |

---

## 👨‍💻 Author

**Axell Rojas**  
*Systems Administrator & AI / Cloud Specialist*  
* 🌐 **Web Portfolio:** [axro-project.vercel.app](https://axro-project.vercel.app/)  
* 💼 **LinkedIn:** [linkedin.com/in/axro](https://www.linkedin.com/in/axro)  
* 🐙 **GitHub:** [@STXNES](https://github.com/STXNES)
