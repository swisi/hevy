import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from hevy_api import HevyClient

load_dotenv()
hevy = HevyClient(os.getenv("HEVY_API_KEY"))
json_data = hevy.get_workouts()

# Dictionary für eigene Übungsbezeichnungen
exercise_names = {
    0: "Rudergerät",
    1: "Latzug",
    2: "Bankdrücken",
    3: "Beinpresse", 
    4: "Butterfly",
    5: "Rudern sitzend",
    6: "Kniestrecker",
    7: "Beinbeuger",
    8: "Rückenstrecken",
    9: "Landmine 180",
    10: "Kreuzheben",
    11: "Kniebeugen"
}

rows = []
exercise_indices = {}

for workout in json_data['workouts']:
    workout_date = workout['start_time'][:10]
    for exercise in workout['exercises']:
        original_title = exercise['title']
        exercise_index = exercise['index']
        custom_title = exercise_names.get(exercise_index, original_title)
        sets = exercise['sets']
        
        if custom_title not in exercise_indices:
            exercise_indices[custom_title] = exercise_index
        
        # ✅ NEU: Unterscheide zwischen Kraft- und Cardio-Übungen
        strength_sets = [s for s in sets if s.get('weight_kg') is not None and s.get('reps') is not None]
        cardio_sets = [s for s in sets if s.get('distance_meters') is not None or s.get('duration_seconds') is not None]
        
        summary = ""
        
        # Krafttraining: Gewicht × Wiederholungen
        if strength_sets:
            weights = [s['weight_kg'] for s in strength_sets]
            reps = [s['reps'] for s in strength_sets]
            set_count = len(strength_sets)
            
            if len(set(weights)) == 1 and len(set(reps)) == 1:
                summary = f"{set_count} × {reps[0]} × {weights[0]}kg"
            else:
                summary = ", ".join([f"{s['weight_kg']}kg×{s['reps']}" for s in strength_sets])
        
        # ✅ NEU: Cardio: Zeit / Distanz
        elif cardio_sets:
            cardio_parts = []
            for s in cardio_sets:
                parts = []
                if s.get('duration_seconds'):
                    minutes = s['duration_seconds'] // 60
                    seconds = s['duration_seconds'] % 60
                    if seconds > 0:
                        parts.append(f"{minutes}:{seconds:02d}min")
                    else:
                        parts.append(f"{minutes}min")
                
                if s.get('distance_meters'):
                    if s['distance_meters'] >= 1000:
                        parts.append(f"{s['distance_meters']/1000:.1f}km")
                    else:
                        parts.append(f"{s['distance_meters']}m")
                
                if parts:
                    cardio_parts.append(" / ".join(parts))
            
            if len(cardio_sets) > 1:
                summary = f"{len(cardio_sets)}× " + ", ".join(cardio_parts)
            else:
                summary = cardio_parts[0] if cardio_parts else ""
        
        rows.append({
            'Date': workout_date,
            'Exercise': custom_title,
            'Summary': summary
        })

df = pd.DataFrame(rows)
pivot_df = df.pivot_table(index="Date", columns="Exercise", values="Summary", aggfunc="first")

# Sortiere Spalten nach Index
sorted_columns = sorted(pivot_df.columns, key=lambda x: exercise_indices.get(x, 999))
pivot_df = pivot_df[sorted_columns]

st.title("Trainingsübersicht kompakt (wie Trainingsblatt)")
st.dataframe(pivot_df.style.set_properties(**{'white-space': 'pre-line'}))
