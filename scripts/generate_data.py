import psycopg2
from faker import Faker
import os

# Database connection details
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin_password")
DB_NAME = os.getenv("POSTGRES_DB", "ecommerce_db")

# Connect to the database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Use Faker to generate realistic data
faker = Faker()

# Store generated emails to avoid duplicates
generated_emails = set()

# Generate and insert 1 million records
batch_size = 10000
total_records = 1000000

for i in range(0, total_records, batch_size):
    records = []
    for _ in range(batch_size):
        email = faker.email()
        # Ensure unique emails
        while email in generated_emails:
            email = faker.email()
        generated_emails.add(email)
        records.append((faker.name(), email, faker.date_time_this_decade()))

    args_str = ','.join(cursor.mogrify("(%s, %s, %s)", record).decode("utf-8") for record in records)
    cursor.execute(f"INSERT INTO customers (name, email, created_at) VALUES {args_str}")
    conn.commit()
    print(f"{i + batch_size} records inserted...")

print("Data generation complete!")
cursor.close()
conn.close()
