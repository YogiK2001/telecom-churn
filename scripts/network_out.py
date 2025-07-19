import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid

# Parameters
num_rows = 20000
tower_ids = [f'TWR{str(i).zfill(3)}' for i in range(1, 101)]
regions = ["North", "South", "East", "West", "Central"]
locations = [f"Location_{i}" for i in range(1, 101)]  # Slightly mismatched
outage_types = ["Power", "Hardware", "Software", "Other", "Unkown", "S0ftware"]
report_sources = ["User", "Admin", "Auto", "Other"]

def random_timestamp_pair():
    start = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23))
    end = start + timedelta(minutes=random.randint(-30, 300))  # some anomalies with negative duration
    return start, end

def generate_outage():
    tower = random.choice(tower_ids)
    region = random.choice(regions)
    location = random.choice(locations) if random.random() > 0.15 else f"Mismatch_{random.randint(1, 10)}"
    outage_start, outage_end = random_timestamp_pair()
    return {
        "outage_id": str(uuid.uuid4()),
        "tower_id": tower,
        "region": region,
        "location": location,
        "outage_start": outage_start.isoformat(),
        "outage_end": outage_end.isoformat(),
        "duration_minutes": round((outage_end - outage_start).total_seconds() / 60, 2),
        "outage_type": random.choice(outage_types),
        "affected_users": max(0, int(np.random.normal(100, 50))),  # avoid negative
        "reported_by": random.choice(report_sources),
    }

# Generate base data
print("Generating base data...")
data = [generate_outage() for _ in range(num_rows)]
df = pd.DataFrame(data)

# Add missing values (~2%)
print("Adding missing values...")
for col in df.columns:
    df.loc[df.sample(frac=0.02).index, col] = np.nan

# Add duplicates (~1%)
print("Adding duplicates...")
duplicates = df.sample(frac=0.01)
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle and export
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv("network_outages.csv", index=False)

print(f"✅ File 'network_outages.csv' created with {df.shape[0]} rows.")
