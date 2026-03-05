import re
import json

# Read receipt file
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Extract prices
prices = re.findall(r"\d+\.\d{2}", text)

# Extract product names (word(s) before price)
products = re.findall(r"([A-Za-z ]+)\s+\d+\.\d{2}", text)

# Calculate total amount
total = sum(float(price) for price in prices)

# Extract date
date_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
date = date_match.group() if date_match else None

# Extract time
time_match = re.search(r"\d{2}:\d{2}", text)
time = time_match.group() if time_match else None

# Find payment method
payment = None
if re.search(r"CARD", text, re.IGNORECASE):
    payment = "CARD"
elif re.search(r"CASH", text, re.IGNORECASE):
    payment = "CASH"
elif re.search(r"VISA", text, re.IGNORECASE):
    payment = "VISA"
elif re.search(r"MASTERCARD", text, re.IGNORECASE):
    payment = "MASTERCARD"

# Create structured output
data = {
    "date": date,
    "time": time,
    "products": products,
    "prices": prices,
    "total_calculated": total,
    "payment_method": payment
}

# Print result in readable JSON format
print(json.dumps(data, indent=4))