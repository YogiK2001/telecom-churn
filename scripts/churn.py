
import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

def generate_data(n_rows=50000):
    data = []

    locations_real = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    locations_anomalous = ['Ney York', 'Loz Angeles', 'Chigaco', 'Huston', 'Pheonix']

    for _ in range(n_rows):
        user_id = fake.uuid4()
        age = random.choice([random.randint(18, 70), None])  # introduce missing values
        gender = random.choice(['Male', 'Female', None])
        income = round(random.uniform(20000, 150000), 2)
        signup_date = fake.date_between(start_date='-5y', end_date='today')
        last_active = fake.date_between(start_date=signup_date, end_date='today')
        location = random.choices(
            locations_real + locations_anomalous,
            weights=[0.85]*len(locations_real) + [0.15]*len(locations_anomalous)
        )[0]
        plan = random.choice(['Basic', 'Standard', 'Premium', None])
        churn_flag = random.choice([0, 1])
        usage_gb = round(random.uniform(0.5, 50.0), 2)
        complaints = random.choice([0, 1, 2, 3, 4, 5])
        is_verified = random.choice([True, False])

        data.append([
            user_id, age, gender, income, signup_date, last_active,
            location, plan, churn_flag, usage_gb, complaints, is_verified
        ])

    columns = [
        'user_id', 'age', 'gender', 'income', 'signup_date', 'last_active',
        'location', 'plan', 'churn_flag', 'usage_gb', 'complaints', 'is_verified'
    ]
    
    df = pd.DataFrame(data, columns=columns)

    # Introduce some duplicate rows (2%)
    duplicates = df.sample(frac=0.02, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)

    return df

# Generate and save
df_churn = generate_data()
df_churn.to_parquet("churn_flag.parquet", index=False)
df_churn.to_csv("churn_flag.csv", index=False)
print("✅ Files created:\n- churn_flag.parquet\n- churn_flag.csv\nWith shape:", df_churn.shape)