import os
import logging
import requests
from datetime import datetime

# Setup logging architecture
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("PlaybetBonusConsumer")

# 1. Configuration Settings
# Replace with your live Render URL if running in production
API_URL = "http://127.0.0.1:8000/api/v1/automation/birthdays"
API_KEY = "playbet_dev_secret_2026"
BONUS_AMOUNT_ZAR = 50.00

# 2. Simulated Endpoints (Where the data gets sent)
# In production, these will point to your SMS Gateway or Playbet Wallet Transaction Engine
SMS_GATEWAY_URL = "https://api.internal.playbet/v1/sms/send"
WALLET_CREDIT_URL = "https://api.internal.playbet/v1/wallet/credit"


def fetch_today_birthdays():
    """Calls your secure cloud API to get filtered, compliance-checked online users."""
    headers = {
        "X-Playbet-Automation-Key": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        logger.info(f"Connecting to birthday data layer at {API_URL}...")
        response = requests.get(API_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to fetch data. Status: {response.status_code}, Error: {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        logger.critical(f"Network error linking to API: {str(e)}")
        return []


def credit_player_wallet(user_id: str, username: str) -> bool:
    """Simulates sending a credit instruction to your core betting engine balance ledger."""
    payload = {
        "user_id": user_id,
        "amount": BONUS_AMOUNT_ZAR,
        "currency": "ZAR",
        "description": f"Automated Birthday Bonus - Generated {datetime.now().strftime('%Y-%m-%d')}"
    }
    
    # --- SIMULATION MODE LOGIC ---
    # In production, change this to an actual requests.post() call against your core system
    logger.info(f" [WALLET SUCCESS] Credited R{BONUS_AMOUNT_ZAR:.2f} to wallet of User: {username} (ID: {user_id})")
    return True


def send_birthday_sms(phone: str, username: str):
    """Simulates sending a promotional SMS notification to the active user."""
    message = f"Happy Birthday {username}! We have credited a R{BONUS_AMOUNT_ZAR:.0f} birthday bonus to your Playbet online account. Enjoy your day! T&Cs apply."
    
    # --- SIMULATION MODE LOGIC ---
    logger.info(f" [SMS SUCCESS] Sent text notification to {phone}: '{message}'")


def main():
    logger.info("Executing daily birthday bonus distribution process...")
    
    # Step A: Fetch targeted users
    birthday_players = fetch_today_birthdays()
    
    if not birthday_players:
        logger.info("No matching eligible online players found celebrating a birthday today. Exiting.")
        return
        
    logger.info(f"Discovered {len(birthday_players)} validated profiles awaiting rewards.")
    processed_count = 0
    
    # Step B: Loop through and execute distributions sequentially
    for player in birthday_players:
        user_id = player["user_id"]
        username = player["username"]
        phone = player["phone"]
        
        # Action 1: Credit Wallet
        wallet_success = credit_player_wallet(user_id, username)
        
        # Action 2: Trigger Notification if wallet transaction succeeded
        if wallet_success:
            send_birthday_sms(phone, username)
            processed_count += 1
            
    logger.info(f"Distribution cycle successfully complete. Total online users rewarded: {processed_count}")


if __name__ == "__main__":
    main()