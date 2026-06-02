import re
from datetime import datetime
from typing import List, Optional
import pandas as pd
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

app = FastAPI(
    title="Playbet Birthday Automation API",
    description="Live microservice connecting directly to our hosted GitHub dataset."
)

# 1. Secure API Key Guardrails (Prevents unauthorized users from pulling data)
API_KEY_NAME = "X-Playbet-Automation-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)
MOCK_SECURE_TOKEN = "playbet_dev_secret_2026"

# 2. YOUR RAW GITHUB LINK
# Replace 'Nicky540-eng' with your actual github username if it's different!
CLOUD_DATA_URL = "https://raw.githubusercontent.com/Nicky540-eng/playbet-birthday-service/main/adavrk_bulk_10k_export.csv"


class BirthdayRewardProfile(BaseModel):
    user_id: str
    username: str
    email: str
    phone: str
    extracted_dob: str
    calculated_age: int
    current_balance: float
    location_channel: str


def parse_sa_id_birthday(id_str: str) -> tuple[Optional[datetime], int]:
    """Extracts date of birth and calculates age from standard 13-digit SA national ID."""
    id_clean = str(id_str).strip().split('.')[0]
    if not id_clean or len(id_clean) < 6 or not re.match(r"^\d+$", id_clean):
        return None, 0
    
    yy, mm, dd = int(id_clean[0:2]), int(id_clean[2:4]), int(id_clean[4:6])
    
    # Check if birth year belongs to 2000s or 1900s
    current_year = datetime.now().year
    century = 2000 if yy <= (current_year - 2000) else 1900
    full_year = century + yy
    
    try:
        dob_date = datetime(full_year, mm, dd)
        age = current_year - dob_date.year - ((datetime.now().month, datetime.now().day) < (dob_date.month, dob_date.day))
        return dob_date, age
    except ValueError:
        return None, 0


@app.get(
    "/api/v1/automation/birthdays",
    response_model=List[BirthdayRewardProfile],
    status_code=status.HTTP_200_OK,
    summary="Extract active online birthdays straight from the cloud dataset."
)
async def extract_and_filter_birthdays(api_key: str = Security(api_key_header)):
    """
    Downloads the 10,000-row file from GitHub, drops retail branch records,
    verifies legal age compliance limits (18+), and isolates users whose birthday is TODAY.
    """
    if api_key != MOCK_SECURE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API Key credentials provided.")

    try:
        # Reach out to the internet and stream the CSV data directly from GitHub
        df = pd.read_csv(CLOUD_DATA_URL)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cloud file: {str(e)}")

    target_rewards = []
    
    # We will use today's date context (June 2nd) to match our testing profiles
    today = datetime.now() 

    for _, row in df.iterrows():
        # Step A: Filter out disabled or inactive accounts
        if str(row["Disabled"]).upper() == "TRUE" or str(row["Deleted"]).upper() == "TRUE":
            continue
        if str(row["Reg. finished"]).upper() != "TRUE" or row["Status"] != "Active":
            continue
            
        # Step B: Filter out retail channel footprints (target online database rows only)
        tags = str(row["Tags"]).lower()
        location = str(row["Location"]).lower()
        if "online" not in tags or "branch" in location or "retail" in tags:
            continue
            
        # Step C: Parse Identity string column into operational birthday values
        dob_datetime, age = parse_sa_id_birthday(row["Identity"])
        if not dob_datetime:
            continue
            
        # Step D: Match checking parameters (Month and Day must match today)
        if dob_datetime.month == today.month and dob_datetime.day == today.day:
            if age >= 18:  # Enforce absolute legal gambling compliance limits
                target_rewards.append(
                    BirthdayRewardProfile(
                        user_id=str(row["ID"]),
                        username=str(row["User"]),
                        email=str(row["Email"]),
                        phone=str(row["Phone"]),
                        extracted_dob=dob_datetime.strftime("%Y-%m-%d"),
                        calculated_age=age,
                        current_balance=float(row["Balance"]),
                        location_channel=str(row["Location"])
                    )
                )

    return target_rewards