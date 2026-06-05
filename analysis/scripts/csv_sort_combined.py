import csv
from datetime import datetime

def is_during_sleep(timestamp, sleep_intervals):
    for start, end in sleep_intervals:
        if start <= timestamp <= end:
            return True
    return False

def to_24_hour(time_text):
    if not time_text:
        return ''
    return datetime.strptime(time_text, '%I:%M:%S %p').strftime('%H:%M')

def read_sleep_data(sleep_file):
    print("Reading sleep data...")
    sleep_intervals = []
    sleep_times = {}
    with open(sleep_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_str = row['sleep_start'].replace(' ', 'T').replace('+0000', '+00:00')
            end_str = row['sleep_end'].replace(' ', 'T').replace('+0000', '+00:00')
            start = datetime.fromisoformat(start_str)
            end = datetime.fromisoformat(end_str)
            sleep_intervals.append((start, end))
            date = end.date()
            if date not in sleep_times:
                sleep_times[date] = {
                    'start': start.strftime('%H:%M'),
                    'end': end.strftime('%H:%M')
                }
    print(f"Loaded {len(sleep_intervals)} sleep periods")
    return sleep_intervals, sleep_times

def read_sleep_score_data(sleep_score_file):
    print("Reading sleep score data...")
    sleep_scores = {}
    with open(sleep_score_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
            date = timestamp.date()
            sleep_scores[date] = int(row['overall_score'])
    print(f"Loaded {len(sleep_scores)} sleep scores")
    return sleep_scores

def read_sleep_stage_data(sleep_stage_file):
    print("Reading sleep stage data...")
    sleep_stages = {}
    with open(sleep_stage_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stage_type = row['sleep_stage_type'].strip().upper()
            if stage_type not in {'REM', 'DEEP'}:
                continue
            start = datetime.fromisoformat(row['sleep_stage_start'].replace(' ', 'T').replace('+0000', '+00:00'))
            end = datetime.fromisoformat(row['sleep_stage_end'].replace(' ', 'T').replace('+0000', '+00:00'))
            date = end.date()
            if date not in sleep_stages:
                sleep_stages[date] = {'rem_minutes': 0.0, 'deep_minutes': 0.0}
            duration_minutes = (end - start).total_seconds() / 60
            if stage_type == 'REM':
                sleep_stages[date]['rem_minutes'] += duration_minutes
            else:
                sleep_stages[date]['deep_minutes'] += duration_minutes
    print(f"Loaded sleep stage totals for {len(sleep_stages)} days")
    return sleep_stages

def read_form_data(form_file, person):
    print("Reading form data...")
    form_data = {}
    with open(form_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Naam'].strip().lower() != person:
                continue
            date = datetime.strptime(row['Wat is de huidige datum'], '%d-%m-%Y').date()
            if date not in form_data:
                form_data[date] = row
    print(f"Loaded {len(form_data)} form rows")
    return form_data

def read_heart_rate_data(heart_rate_dir, heart_rate_files):
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
    return heart_rate_data

def read_steps_data(steps_file):
    print("Reading steps data...")
    steps_data = []
    with open(steps_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
            steps = int(row['steps'])
            steps_data.append((timestamp, steps))
    print(f"Loaded {len(steps_data)} step measurements")
    return steps_data

def read_calories_data(calories_file):
    print("Reading calories data...")
    daily_calories = {}
    try:
        with open(calories_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
                date = timestamp.date()
                calories = float(row['Kilocalories'])
                if date not in daily_calories:
                    daily_calories[date] = 0
                daily_calories[date] += calories
    except FileNotFoundError:
        pass
    print(f"Loaded calories for {len(daily_calories)} days")
    return daily_calories


def process_person(person):
    sleep_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Health Fitness Data_GoogleData/UserSleeps_2026-05-06.csv"
    sleep_stage_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Health Fitness Data_GoogleData/UserSleepStages_2026-05-06.csv"
    sleep_score_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Sleep Score/sleep_score.csv"
    steps_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData/steps_2026-05-01.csv"
    heart_rate_dir = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData"
    form_file = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/betere Naamloos formulier (Antwoorden)(3).csv"
    calories_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData/active_energy_burned.csv"
    if person == 'lucas':
        calories_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData/active_energy_burned_2026-05-01.csv"

    heart_rate_files = [
        "heart_rate_2026-04-06.csv", "heart_rate_2026-05-06.csv", "heart_rate_2026-05-07.csv",
        "heart_rate_2026-05-08.csv", "heart_rate_2026-05-09.csv", "heart_rate_2026-05-10.csv",
        "heart_rate_2026-05-11.csv", "heart_rate_2026-05-12.csv", "heart_rate_2026-05-13.csv",
        "heart_rate_2026-05-14.csv", "heart_rate_2026-05-15.csv", "heart_rate_2026-05-16.csv",
        "heart_rate_2026-05-17.csv", "heart_rate_2026-05-18.csv", "heart_rate_2026-05-19.csv",
        "heart_rate_2026-05-20.csv", "heart_rate_2026-05-21.csv",
    ]

    sleep_intervals, sleep_times = read_sleep_data(sleep_file)
    sleep_stage_totals = read_sleep_stage_data(sleep_stage_file)
    sleep_scores = read_sleep_score_data(sleep_score_file)
    form_data = read_form_data(form_file, person)
    heart_rate_data = read_heart_rate_data(heart_rate_dir, heart_rate_files)
    steps_data = read_steps_data(steps_file)
    daily_calories = read_calories_data(calories_file)

    print(f"Filtering out measurements during sleep for {person}...")
    awake_heart_rate = [(ts, bpm) for ts, bpm in heart_rate_data
                        if not is_during_sleep(ts, sleep_intervals)]

    daily_data = {}
    for timestamp, bpm in awake_heart_rate:
        date = timestamp.date()
        if date not in daily_data:
            daily_data[date] = {'heart_rates': [], 'min_hr': bpm, 'max_hr': bpm}
        daily_data[date]['heart_rates'].append(bpm)
        daily_data[date]['min_hr'] = min(daily_data[date]['min_hr'], bpm)
        daily_data[date]['max_hr'] = max(daily_data[date]['max_hr'], bpm)

    daily_steps = {}
    for timestamp, steps in steps_data:
        date = timestamp.date()
        if date not in daily_steps:
            daily_steps[date] = 0
        daily_steps[date] += steps

    person_results = []
    person_sleep_score_results = []
    
    for date in sorted(daily_data.keys()):
        if date in daily_steps:
            avg_hr = sum(daily_data[date]['heart_rates']) / len(daily_data[date]['heart_rates'])
            form_row = form_data.get(date, {})
            if form_row:
                phone_time = to_24_hour(form_row['Hoelaat heb je voor het laatst op je telefoon gezeten?'])
                meal_time = to_24_hour(form_row['Wanneer heb je voor het laatst gegeten?'])
                meal_type = form_row['Wat was het?']
            else:
                phone_time = ''
                meal_time = ''
                meal_type = ''
                
            row_data = {
                'naam': person.capitalize(),
                'date': date,
                'average_heart_rate': round(avg_hr, 2),
                'min_heart_rate': daily_data[date]['min_hr'],
                'max_heart_rate': daily_data[date]['max_hr'],
                'start': sleep_times.get(date, {}).get('start', ''),
                'end': sleep_times.get(date, {}).get('end', ''),
                'rem_sleep_minutes': round(sleep_stage_totals.get(date, {}).get('rem_minutes', 0), 2),
                'deep_sleep_minutes': round(sleep_stage_totals.get(date, {}).get('deep_minutes', 0), 2),
                'sleep_score': sleep_scores.get(date, ''),
                'calories_burned': round(daily_calories.get(date, 0), 2),
                'total_steps': daily_steps[date],
                'phone_last_used': phone_time,
                'last_food_time': meal_time,
                'last_food': meal_type,
            }
            
            person_results.append(row_data)
            if date in sleep_scores:
                person_sleep_score_results.append(row_data)

    return person_results, person_sleep_score_results


# Centraliseer dataverzameling voor alle personen
all_results = []
all_sleep_score_results = []

person_names = ['robin', 'mohammed', 'lucas']
for person in person_names:
    print(f"\n--- Processing {person.upper()} ---")
    p_res, p_ss_res = process_person(person)
    all_results.extend(p_res)
    all_sleep_score_results.extend(p_ss_res)

# Bestemmingsmappen instellen
output_dir_raw = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/combined_raw"
output_dir_filtered = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/combined_filetered"

output_file_raw = f"{output_dir_raw}/combined_raw.csv"
sleep_score_output_file = f"{output_dir_filtered}/combined_data_filtered.csv"

fieldnames = ['naam', 'date', 'average_heart_rate', 'min_heart_rate', 'max_heart_rate', 'start', 'end', 'rem_sleep_minutes', 'deep_sleep_minutes', 'sleep_score', 'calories_burned', 'total_steps', 'phone_last_used', 'last_food_time', 'last_food']

print(f"\nSaving merged raw data to {output_file_raw}...")
with open(output_file_raw, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_results)

print(f"Saving merged sleep score data to {sleep_score_output_file}...")
with open(sleep_score_output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_sleep_score_results)

print(f"\nDone. Combined dataset contains {len(all_results)} total rows.")