import streamlit as st

# Define the pages
seite1 = st.Page("seite1.py", title="Workouts", icon="")#"🎈")
seite2 = st.Page("seite2.py", title="Seite 2", icon="")#"❄️")
seite3 = st.Page("seite3.py", title="Seite 3", icon="")#"🎉")

# Set up navigation
pg = st.navigation([seite1, seite2, seite3])

# Run the selected page
pg.run()