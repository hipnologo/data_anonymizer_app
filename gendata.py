import csv
from faker import Faker
import random

# Create a Faker generator
fake = Faker()

# Function to generate a random phone number with extensions
def random_phone():
    pattern = random.choice(["###-###-####x####", "+1-###-###-####x####", "###.###.####x####"])
    return fake.numerify(text=pattern)

# Function to generate a random entry
def generate_entry():
    return {
        "Name": fake.name(),
        "Email": fake.email(),
        "Phone": random_phone(),
        "Age": random.randint(18, 90),
        "Address": fake.address().replace("\n", ", ")
    }

# Generate 100 entries
entries = [generate_entry() for _ in range(100)]

# Writing to CSV
with open('data/random_data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Email", "Phone", "Age", "Address"])
    writer.writeheader()
    for entry in entries:
        writer.writerow(entry)

print("CSV file 'data/random_data.csv' has been created with 100 random entries.")
