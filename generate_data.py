import random
from datetime import datetime, timedelta
import pandas as pd

print("Generating 10,000 mock Adavrk records...")

branches = ["Malvern Branch", "Potchefstroom Branch", "Pretoria Branch", "Randburg Branch", "White River Branch"]
digital_locations = ["Web Portal", "Mobile App", "iOS App", "Android App"]
statuses = ["Active", "Suspended", "Dormant"]
cities = ["Johannesburg", "Pretoria", "Cape Town", "Durban", "Potchefstroom"]

first_names = ["Thabo", "Sipho", "Pieter", "Johan", "Naledi", "Zama", "David", "Michael", "Sarah"]
last_names = ["Khumalo", "Botha", "Van der Merwe", "Ndlovu", "Zulu", "Smith", "Mokoena"]

data = []

# Generate 10,000 records
for i in range(10000):
    user_id = f"PL{10000 + i}"
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    username = f"{fn.lower()}_{ln.lower()}{random.randint(10, 99)}"
    email = f"{username}@example.co.za"
    phone = f"+27{random.choice([60, 71, 82])}{random.randint(1000000, 9999999)}"
    
    is_online = random.random() < 0.75
    tags = ["online", "sportsbook"] if is_online else ["retail"]
    location = random.choice(digital_locations) if is_online else random.choice(branches)
    
    # Mix of random birthdays and some set specifically to June 2nd for automation testing
    if i < 150:
        birth_month, birth_day = 6, 2
        birth_year = random.randint(1980, 2005)
    else:
        birth_year = random.randint(1965, 2007)
        birth_month, birth_day = random.randint(1, 12), random.randint(1, 28)
        
    dob = datetime(birth_year, birth_month, birth_day)
    identity_str = f"{dob.strftime('%y%m%d')}5123081" # Valid SA ID prefix format
    
    record = {
        "ID": user_id, "User": username, "Email": email, "Phone": phone,
        "Tags": ",".join(tags), "Extra data": "{}", 
        "Registered At": "2024-01-01 10:00:00", "Last Login": "2026-06-01 14:20:00",
        "City": random.choice(cities), "Currency": "ZAR", "Balance": round(random.uniform(50, 3000), 2),
        "Reg. finished": "TRUE", "Identity": identity_str, "Location": location,
        "Disabled": "FALSE", "Deleted": "FALSE", "Last deposit": "2026-05-15", "Status": "Active"
    }
    data.append(record)

df = pd.DataFrame(data)
df.to_csv("adavrk_bulk_10k_export.csv", index=False)
print("Success! File saved as 'adavrk_bulk_10k_export.csv'")