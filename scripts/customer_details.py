import random
import json
from faker import Faker
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

fake = Faker()
num_rows = 50000  # 1/10th of 500K

regions = ["North", "South", "East", "West", "Central", "Unknown"]
devices = ["Mobile", "Laptop", "Tablet", "Desktop"]
genders = ["M", "F", "Unknown", "X", "Malee", "Fem"]  # Include minor anomalies

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_customer():
    age = random.choice([random.randint(18, 70), 5, 120]) if random.random() < 0.03 else random.randint(18, 70)
    gender = random.choice(genders)
    region = random.choice(regions + ["Northeast", "Central West"])  # anomalies
    return {
        "customer_id": fake.uuid4(),
        "name": fake.name(),
        "age": age,
        "gender": gender,
        "income": round(random.uniform(200000, 2000000), 2),
        "region": region,
        "signup_date": fake.date_between(start_date='-3y', end_date='-1y').isoformat(),
        "last_login": fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
        "preferred_device": random.choice(devices),
        "loyalty_points": random.randint(0, 10000)
    }

# Generate base dataset
print("Generating base data...")
data = [generate_customer() for _ in range(num_rows)]

# Convert to DataFrame for easy manipulation
df = pd.DataFrame(data)

# Add missing values (~2% of total cells)
print("Adding missing values...")
for col in df.columns:
    df.loc[df.sample(frac=0.02).index, col] = np.nan

# Add duplicates (~1%)
print("Adding duplicates...")
df_duplicates = df.sample(frac=0.01)
df = pd.concat([df, df_duplicates], ignore_index=True)

# Shuffle and convert to list of dicts
df = df.sample(frac=1).reset_index(drop=True)
final_data = df.to_dict(orient='records')

# Save as JSON
output_file = "customer_details.json"
with open(output_file, "w") as f:
    json.dump(final_data, f, indent=4)

print(f"✅ Dataset created: {output_file} with {len(final_data)} records.")