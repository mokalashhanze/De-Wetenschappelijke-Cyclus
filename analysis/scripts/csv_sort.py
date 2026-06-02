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
    sleep_score_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Sleep Score/sleep_score.csv"
    steps_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData/steps_2026-05-01.csv"
    output_dir = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/combined_raw"
    sleep_score_output_dir = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/combined_filetered"
    output_file = f"{output_dir}/combined_data_{person}.csv"
    sleep_score_output_file = f"{sleep_score_output_dir}/combined_data_{person}.csv"
    heart_rate_dir = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData"
    form_file = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/betere Naamloos formulier (Antwoorden)(3).csv"
    calories_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData/active_energy_burned.csv"
    if person == 'lucas':
        calories_file = f"/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/raw_data/takeout_{person}/Fitbit/Physical Activity_GoogleData/active_energy_burned_2026-05-01.csv"

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
        "heart_rate_2026-05-16.csv",
        "heart_rate_2026-05-17.csv",
        "heart_rate_2026-05-18.csv",
        "heart_rate_2026-05-19.csv",
        "heart_rate_2026-05-20.csv",
        "heart_rate_2026-05-21.csv",
    ]

    sleep_intervals, sleep_times = read_sleep_data(sleep_file)
    sleep_scores = read_sleep_score_data(sleep_score_file)
    form_data = read_form_data(form_file, person)
    heart_rate_data = read_heart_rate_data(heart_rate_dir, heart_rate_files)
    steps_data = read_steps_data(steps_file)
    daily_calories = read_calories_data(calories_file)

    print("Filtering out measurements during sleep...")
    awake_heart_rate = [(ts, bpm) for ts, bpm in heart_rate_data
                        if not is_during_sleep(ts, sleep_intervals)]
    print(f"Measurements during sleep: {len(heart_rate_data) - len(awake_heart_rate)}")
    print(f"Measurements while awake: {len(awake_heart_rate)}")

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

    results = []
    sleep_score_results = []
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
            results.append({
                'date': date,
                'average_heart_rate': round(avg_hr, 2),
                'min_heart_rate': daily_data[date]['min_hr'],
                'max_heart_rate': daily_data[date]['max_hr'],
                'start': sleep_times.get(date, {}).get('start', ''),
                'end': sleep_times.get(date, {}).get('end', ''),
                'sleep_score': sleep_scores.get(date, ''),
                'calories_burned': round(daily_calories.get(date, 0), 2),
                'total_steps': daily_steps[date],
                'phone_last_used': phone_time,
                'last_food_time': meal_time,
                'last_food': meal_type,
            })
            if date in sleep_scores:
                sleep_score_results.append({
                    'date': date,
                    'average_heart_rate': round(avg_hr, 2),
                    'min_heart_rate': daily_data[date]['min_hr'],
                    'max_heart_rate': daily_data[date]['max_hr'],
                    'start': sleep_times.get(date, {}).get('start', ''),
                    'end': sleep_times.get(date, {}).get('end', ''),
                    'sleep_score': sleep_scores.get(date, ''),
                    'calories_burned': round(daily_calories.get(date, 0), 2),
                    'total_steps': daily_steps[date],
                    'phone_last_used': phone_time,
                    'last_food_time': meal_time,
                    'last_food': meal_type,
                })

    print(f"Saving results to {output_file}...")
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['date', 'average_heart_rate', 'min_heart_rate', 'max_heart_rate', 'start', 'end', 'sleep_score', 'calories_burned', 'total_steps', 'phone_last_used', 'last_food_time', 'last_food']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saving sleep score results to {sleep_score_output_file}...")
    with open(sleep_score_output_file, 'w', newline='') as f:
        fieldnames = ['date', 'average_heart_rate', 'min_heart_rate', 'max_heart_rate', 'start', 'end', 'sleep_score', 'calories_burned', 'total_steps', 'phone_last_used', 'last_food_time', 'last_food']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sleep_score_results)

    print(f"Done. Created {len(results)} daily datasets.")


person_names = ['robin', 'mohammed', 'lucas']
for person in person_names:
    process_person(person)
