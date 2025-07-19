# recharge_history.parquet
import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()
np.random.seed(42)
random.seed(42)

# Total rows (1/10th of 1.1M)
num_rows = 110_000

# Helper function for location mismatch
def random_location_mismatch(loc):
    if random.random() < 0.05:  # 5% mismatch
        return fake.city()
    return loc

# Generate synthetic data
def generate_recharge_data(n):
    user_ids = [fake.uuid4() for _ in range(n)]
    timestamps = [fake.date_time_between(start_date='-1y', end_date='now') for _ in range(n)]
    recharge_types = np.random.choice(['Prepaid', 'Postpaid'], size=n)
    amounts = np.round(np.random.normal(loc=199, scale=100, size=n), 2)
    amounts = np.clip(amounts, 10, 999)
    plan_names = np.random.choice(['Combo199', 'Data249', 'TalkTime99', 'Unlimited499'], size=n)
    payment_methods = np.random.choice(['UPI', 'Credit Card', 'Debit Card', 'Wallet'], size=n)
    locations = [fake.city() for _ in range(n)]
    reported_locations = [random_location_mismatch(loc) for loc in locations]
    device_types = np.random.choice(['Android', 'iOS', 'Feature Phone'], size=n)
    statuses = np.random.choice(['Success', 'Failed'], size=n, p=[0.95, 0.05])
    
    df = pd.DataFrame({
        'user_id': user_ids,
        'timestamp': timestamps,
        'recharge_type': recharge_types,
        'amount': amounts,
        'plan_name': plan_names,
        'payment_method': payment_methods,
        'location': locations,
        'reported_location': reported_locations,
        'device_type': device_types,
        'status': statuses
    })

    # Inject missing values
    for col in ['amount', 'location', 'payment_method']:
        df.loc[df.sample(frac=0.02).index, col] = np.nan  # 2% missing
    
    # Inject duplicates
    df = pd.concat([df, df.sample(frac=0.03)], ignore_index=True)  # 3% duplicates

    return df

# Generate and save to CSV
df = generate_recharge_data(num_rows)
df.to_csv("recharge_history.csv", index=False)

print("✅ Dataset saved as 'recharge_history.csv' in your local directory.")