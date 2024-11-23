"""Generate a CSV file with the first Fridays of each month from November 2024 down to January 2007 in reverse chronological order."""

import csv
from datetime import datetime, timedelta


def first_friday(year: str, month: str) -> datetime:
    """Return the first Friday of the month."""
    first_day = datetime(year, month, 1)
    # Calculate the first Friday
    days_until_friday = (4 - first_day.weekday() + 7) % 7
    return first_day + timedelta(days=days_until_friday)


full_first_fridays_reversed = []

for year in range(2024, 2006, -1):
    for month in range(12, 0, -1):
        date = first_friday(year, month).strftime("%Y-%m-%d")
        full_first_fridays_reversed.append(date)

# Save to CSV
csv_filename = "first_fridays.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date"])
    for date in full_first_fridays_reversed:
        writer.writerow([date])

print(f"CSV file '{csv_filename}' created successfully.")
