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
    time_text = time_text.strip()
    try:
        return datetime.strptime(time_text, '%I:%M:%S %p').strftime('%H:%M')
    except ValueError:
        try:
            return datetime.strptime(time_text, '%I:%M %p').strftime('%H:%M')
        except ValueError:
            return time_text

def calculate_corrected_score(sleep_score, sleep_duration_hours):
    if sleep_score == '' or sleep_duration_hours == '' or sleep_duration_hours <= 0:
        return ''
    actual_hours = float(sleep_duration_hours)
    effective_hours = max(min(actual_hours, 9.0), 6.0)
    duration_factor = effective_hours / 8.0
    return round(float(sleep_score) / duration_factor, 2)

def calculate_sleep_duration(start_str, end_str):
    if not start_str or not end_str:
        return ''
    try:
        t_start = datetime.strptime(start_str, '%H:%M')
        t_end = datetime.strptime(end_str, '%H:%M')
        diff_minutes = (t_end - t_start).total_seconds() / 60.0
        if diff_minutes < 0:
            diff_minutes += 1440
        return round(diff_minutes / 60.0, 2)
    except ValueError:
        return ''

def read_sleep_data(sleep_file):
    print("Reading sleep data...")
    sleep_intervals = []
    sleep_times = {}
    try:
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
                    sleep_times[date] = {'start': start.strftime('%H:%M'), 'end': end.strftime('%H:%M')}
    except (FileNotFoundError, KeyError, ValueError):
        pass
    return sleep_intervals, sleep_times

def read_sleep_score_data(sleep_score_file):
    print("Reading sleep score data...")
    sleep_scores = {}
    try:
        with open(sleep_score_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
                date = timestamp.date()
                sleep_scores[date] = int(row['overall_score'])
    except (FileNotFoundError, KeyError, ValueError):
        pass
    return sleep_scores

def read_sleep_stage_data(sleep_stage_file):
    print("Reading sleep stage data...")
    sleep_stages = {}
    try:
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
    except (FileNotFoundError, KeyError, ValueError):
        pass
    return sleep_stages

def read_form_data(form_file, person):
    print("Reading form data...")
    form_data = {}
    try:
        with open(form_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Naam'].strip().lower() != person:
                    continue
                date = datetime.strptime(row['Wat is de huidige datum'], '%d-%m-%Y').date()
                form_data[date] = row
    except (FileNotFoundError, KeyError, ValueError):
        pass
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
        except (FileNotFoundError, KeyError, ValueError):
            pass
    return heart_rate_data

def read_steps_data(steps_file):
    print("Reading steps data...")
    steps_data = []
    try:
        with open(steps_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00'))
                steps = int(row['steps'])
                steps_data.append((timestamp, steps))
    except (FileNotFoundError, KeyError, ValueError):
        pass
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
                daily_calories[date] = daily_calories.get(date, 0) + calories
    except (FileNotFoundError, KeyError, ValueError):
        pass
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

    heart_rate_files = ["heart_rate_2026-04-06.csv"] + [f"heart_rate_2026-05-{i:02d}.csv" for i in range(6, 22)]

    sleep_intervals, sleep_times = read_sleep_data(sleep_file)
    sleep_stage_totals = read_sleep_stage_data(sleep_stage_file)
    sleep_scores = read_sleep_score_data(sleep_score_file)
    form_data = read_form_data(form_file, person)
    heart_rate_data = read_heart_rate_data(heart_rate_dir, heart_rate_files)
    steps_data = read_steps_data(steps_file)
    daily_calories = read_calories_data(calories_file)

    awake_heart_rate = [(ts, bpm) for ts, bpm in heart_rate_data if not is_during_sleep(ts, sleep_intervals)]
    sleep_heart_rate = [(ts, bpm) for ts, bpm in heart_rate_data if is_during_sleep(ts, sleep_intervals)]

    daily_data = {}
    for timestamp, bpm in awake_heart_rate:
        date = timestamp.date()
        if date not in daily_data:
            daily_data[date] = {'heart_rates': [], 'min_hr': bpm, 'max_hr': bpm}
        daily_data[date]['heart_rates'].append(bpm)
        daily_data[date]['min_hr'] = min(daily_data[date]['min_hr'], bpm)
        daily_data[date]['max_hr'] = max(daily_data[date]['max_hr'], bpm)

    daily_sleep_hr = {}
    for timestamp, bpm in sleep_heart_rate:
        date = timestamp.date()
        daily_sleep_hr.setdefault(date, []).append(bpm)

    daily_steps = {}
    for timestamp, steps in steps_data:
        daily_steps[timestamp.date()] = daily_steps.get(timestamp.date(), 0) + steps

    person_results = []
    person_sleep_score_results = []

    for date in sorted(daily_data.keys()):
        if date in daily_steps:
            avg_hr = sum(daily_data[date]['heart_rates']) / len(daily_data[date]['heart_rates'])
            avg_sleep_hr = (
                round(sum(daily_sleep_hr[date]) / len(daily_sleep_hr[date]), 2)
                if date in daily_sleep_hr else ''
            )

            form_row = form_data.get(date, {})
            duration = calculate_sleep_duration(
                sleep_times.get(date, {}).get('start', ''),
                sleep_times.get(date, {}).get('end', '')
            )
            raw_score = sleep_scores.get(date, '')
            corr_score = calculate_corrected_score(raw_score, duration)

            row_data = {
                'naam': person.capitalize(),
                'date': date,
                'average_heart_rate': round(avg_hr, 2),
                'average_sleep_heart_rate': avg_sleep_hr,
                'min_heart_rate': daily_data[date]['min_hr'],
                'max_heart_rate': daily_data[date]['max_hr'],
                'start': sleep_times.get(date, {}).get('start', ''),
                'end': sleep_times.get(date, {}).get('end', ''),
                'rem_sleep_minutes': round(sleep_stage_totals.get(date, {}).get('rem_minutes', 0), 2),
                'deep_sleep_minutes': round(sleep_stage_totals.get(date, {}).get('deep_minutes', 0), 2),
                'sleep_score': raw_score,
                'sleep_duration_hours': duration,
                'corrected_sleep_score': corr_score,
                'calories_burned': round(daily_calories.get(date, 0), 2),
                'total_steps': daily_steps[date],
                'phone_last_used': to_24_hour(form_row.get('Hoelaat heb je voor het laatst op je telefoon gezeten?', '')),
                'last_food_time': to_24_hour(form_row.get('Wanneer heb je voor het laatst gegeten?', '')),
                'last_food': form_row.get('Wat was het?', '')
            }

            person_results.append(row_data)
            if date in sleep_scores:
                person_sleep_score_results.append(row_data)

    return person_results, person_sleep_score_results

all_results, all_sleep_score_results = [], []
for person in ['robin', 'mohammed', 'lucas']:
    p_res, p_ss_res = process_person(person)
    all_results.extend(p_res)
    all_sleep_score_results.extend(p_ss_res)

output_file_raw = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/combined_data/combined_data.csv"
sleep_score_output_file = "/Users/robinoffringa/Desktop/De-Wetenschappelijke-Cyclus/analysis/data/combined_data_filtered/combined_data_filtered.csv"

fieldnames = [
    'naam', 'date',
    'average_heart_rate',
    'average_sleep_heart_rate',
    'min_heart_rate', 'max_heart_rate',
    'start', 'end',
    'rem_sleep_minutes', 'deep_sleep_minutes',
    'sleep_score', 'sleep_duration_hours', 'corrected_sleep_score',
    'calories_burned', 'total_steps',
    'phone_last_used', 'last_food_time', 'last_food'
]

with open(output_file_raw, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_results)

with open(sleep_score_output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_sleep_score_results)