import os
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from hevy_api import HevyClient

load_dotenv()

# API-Client initialisieren
hevy = HevyClient(os.getenv("HEVY_API_KEY"))

# Beispielaufruf mit deinem API-Key

json_data = hevy.get_workouts()
total_workouts = json_data.get('total_workouts', 0)
#print(f"Anzahl der Workouts: {total_workouts}")
#print(f"Daten: {json_data}")

# Daten für die Tabelle vorbereiten
rows = []
for workout in json_data['workouts']:
    workout_title = workout['title']
    start_time = workout['start_time']
    end_time = workout['end_time']
    for exercise in workout['exercises']:
        exercise_title = exercise['title']
        setcount=0
        for s in exercise['sets']:
            setcount += 1
            row = {
                'Workout Title': workout_title,
                'Start Time': start_time,
                'End Time': end_time,
                'Exercise Title': exercise_title,
                'Set Index': s['index'],
                'Weight (kg)': s['weight_kg'],
                'Reps': s['reps'],
                'Distance (m)': s['distance_meters'],
                'Duration (s)': s['duration_seconds']
            }
            rows.append(row)

#print(f"Workout: {workout_title}")


# DataFrame erstellen
df = pd.DataFrame(rows)

# Tabelle in Streamlit anzeigen
st.title(f"Hevy Workouts: {workout_title}")
st.dataframe(df)