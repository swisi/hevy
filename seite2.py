import pandas as pd
import streamlit as st
from hevy_api import HevyClient
import os

# Hevy-API initialisieren
hevy = HevyClient(os.getenv("HEVY_API_KEY"))
json_data = hevy.get_workouts()

# Daten vorbereiten
rows = []
for workout in json_data['workouts']:
    workout_date = workout['start_time'][:10]
    for exercise in workout['exercises']:
        title = exercise['title']
        sets = exercise['sets']
        set_strs = []
        for s in sets:
            if s.get('weight_kg') is not None and s.get('reps') is not None:
                set_strs.append(f"{s['weight_kg']}kg x {s['reps']}")
            elif s.get('distance_meters') is not None:
                set_strs.append(f"{s['distance_meters']}m")
        set_summary = "\n".join(set_strs)
        rows.append({
            'Date': workout_date,
            'Exercise': title,
            'Sets': set_summary
        })

df = pd.DataFrame(rows)

# Pivotieren: Jede Übung eine Spalte, Werte sind die Sets als String
pivot_df = df.pivot_table(index='Date', columns='Exercise', values='Sets', aggfunc=lambda x: "\n".join(x))

# Optional: Sortiere Übungen alphabetisch
pivot_df = pivot_df.sort_index(axis=1)

st.title("Trainingsübersicht wie auf dem Trainingsblatt")
st.dataframe(pivot_df.style.set_properties(**{'white-space': 'pre-line'}))

# Main page content
st.markdown("# Seite 2 ❄️")
st.sidebar.markdown("# Seite 2 ❄️")