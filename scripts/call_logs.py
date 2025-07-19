import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Parameters
num_rows = 250000  # 1/10th of 2.5M

# Sample data
tower_ids = [f'TWR{str(i).zfill(3)}' for i in range(1, 51)]
locations = [f"Location_{i}" for i in range(1, 51)]  # Intentional mismatch potential

# Helper functions
def random_phone_number():
    return f"+91{random.randint(6000000000, 9999999999)}"

def random_date():
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def generate_row():
    tower = random.choice(tower_ids)
    # Introduce mismatch anomaly: 20% chance of random location
    location = random.choice(locations) if random.random() > 0.2 else locations[tower_ids.index(tower)]
    return {
        "call_id": random.randint(10000000, 99999999),
        "caller_number": random_phone_number(),
        "receiver_number": random_phone_number(),
        "call_duration": round(abs(np.random.normal(180, 120))),  # mean=3min, some noise
        "call_type": random.choice(["Incoming", "Outgoing"]),
        "tower_id": tower,
        "location": location,
        "timestamp": random_date(),
        "dropped_call": random.choice(["Yes", "No"]),
        "signal_strength": round(random.uniform(-120, -30), 1),
    }

# Generate dataset
print("Generating base data...")
data = [generate_row() for _ in range(num_rows)]

# Convert to DataFrame
df = pd.DataFrame(data)

# Introduce missing values randomly (~2% of total values)
print("Introducing missing values...")
for col in df.columns:
    df.loc[df.sample(frac=0.02).index, col] = np.nan

# Add duplicate rows (~1%)
print("Adding duplicates...")
duplicates = df.sample(frac=0.01)
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle rows
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
filename = "call_logs_2024.csv"
df.to_csv(filename, index=False)
print(f"✅ Dataset generated and saved as {filename} with {df.shape[0]} rows.")