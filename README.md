# Playbet Birthday Bonus Automation Service 🎂

This microservice handles the end-to-end data processing pipeline for automatically identifying, validating, and rewarding online users celebrating a birthday today. It completely isolates digital players from retail branch operations to streamline marketing budgets and maintain gambling compliance regulations.

## 🏗️ System Architecture Overview 
## 📋 File Layout Description

* `adavrk_bulk_10k_export.csv`: A mock operational database export containing 10,000 player records with standard Adavrk data attributes.
* `app.py`: A cloud-deployed FastAPI engine that targets, transforms, and matches South African National Identity configurations dynamically over the web.
* `run_daily_bonus.py`: The execution cron machine that reads validated targets, pushes real-time credits to accounts, and triggers SMS promotional campaigns.

## 🚀 Local Installation & Execution

### 1. Initialize Your Workspace
```bash
# Clone or open your workspace directory
cd playbet-birthday-service

# Build and activate your library isolation box
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependency frameworks
pip install fastapi uvicorn pandas requests pydantic