import csv
from datetime import datetime

# File paths
sleep_file = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_robin/Fitbit/Health Fitness Data_GoogleData/UserSleeps_2026-05-06.csv"
steps_file = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_robin/Fitbit/Physical Activity_GoogleData/steps_2026-05-01.csv"
output_file = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/combined_data_robin.csv"
heart_rate_dir = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_robin/Fitbit/Physical Activity_GoogleData"

# Heart rate files
heart_rate_files = [
    "heart_rate_2026-04-06.csv",
    "heart_rate_2026-05-06.csv",
    "heart_rate_2026-05-07.csv",
    "heart_rate_2026-05-08.csv",
    "heart_rate_2026-05-09.csv",
    "heart_rate_2026-05-10.csv",
    "heart_rate_2026-05-11.csv",
    "heart_rate_2026-05-12.csv",
    "heart_rate_2026-05-13.csv",
    "heart_rate_2026-05-14.csv",
    "heart_rate_2026-05-15.csv",
]

# Read sleep data
print("Reading sleep data...")
sleep_intervals = []
with open(sleep_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # make format "2026-05-06 22:50:00+0000"
        start_str = row['sleep_start'].replace(' ', 'T').replace('+0000', '+00:00')
        end_str = row['sleep_end'].replace(' ', 'T').replace('+0000', '+00:00')
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
        sleep_intervals.append((start, end))
print(f"Loaded {len(sleep_intervals)} sleep periods")

# Read heart rate data
print("Reading heart rate files...")
heart_rate_data = []
for filename in heart_rate_files:
    filepath = f"{heart_rate_dir}/{filename}"
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
                bpm = float(row['beats per minute'])
                heart_rate_data.append((timestamp, bpm))
    except FileNotFoundError:
        pass

print(f"Loaded {len(heart_rate_data)} heart rate measurements")

# Read steps data
print("Reading steps data...")
steps_data = []
with open(steps_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
        steps = int(row['steps'])
        steps_data.append((timestamp, steps))
print(f"Loaded {len(steps_data)} step measurements")

# Filter out sleep periods
def is_during_sleep(timestamp, sleep_intervals):
    for start, end in sleep_intervals:
        if start <= timestamp <= end:
            return True
    return False

print("Filtering out measurements during sleep...")
awake_heart_rate = [(ts, bpm) for ts, bpm in heart_rate_data 
                    if not is_during_sleep(ts, sleep_intervals)]
print(f"Measurements during sleep: {len(heart_rate_data) - len(awake_heart_rate)}")
print(f"Measurements while awake: {len(awake_heart_rate)}")

# Calculate daily averages
daily_data = {}
for timestamp, bpm in awake_heart_rate:
    date = timestamp.date()
    if date not in daily_data:
        daily_data[date] = {'heart_rates': [], 'min_hr': bpm, 'max_hr': bpm}
    daily_data[date]['heart_rates'].append(bpm)
    daily_data[date]['min_hr'] = min(daily_data[date]['min_hr'], bpm)
    daily_data[date]['max_hr'] = max(daily_data[date]['max_hr'], bpm)

# Calculate daily steps
daily_steps = {}
for timestamp, steps in steps_data:
    date = timestamp.date()
    if date not in daily_steps:
        daily_steps[date] = 0
    daily_steps[date] += steps

# Combine data - only keep days with steps data
results = []
for date in sorted(daily_data.keys()):
    if date in daily_steps:
        avg_hr = sum(daily_data[date]['heart_rates']) / len(daily_data[date]['heart_rates'])
        results.append({
            'date': date,
            'average_heart_rate': round(avg_hr, 2),
            'min_heart_rate': daily_data[date]['min_hr'],
            'max_heart_rate': daily_data[date]['max_hr'],
            'measurements': len(daily_data[date]['heart_rates']),
            'total_steps': daily_steps[date]
        })

# Write output
print(f"Saving results to {output_file}...")
with open(output_file, 'w', newline='') as f:
    fieldnames = ['date', 'average_heart_rate', 'min_heart_rate', 'max_heart_rate', 'measurements', 'total_steps']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"Done. Created {len(results)} daily datasets.")
