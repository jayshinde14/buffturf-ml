import pandas as pd
from sklearn.neighbors import NearestNeighbors
import joblib
from sqlalchemy import create_engine

import os
# 1. Connect to MySQL Database directly
print("Connecting to the database...")
db_url = os.getenv("DB_URL", "mysql+pymysql://root@localhost:3306/buffturf_db")
engine = create_engine(db_url)

# 2. Fetch booking data using a SQL query
# We need users, turfs, and slots they booked. We only want CONFIRMED or COMPLETED bookings.
query = """
    SELECT b.user_id, b.turf_id, bs.slot_id
    FROM bookings b
    JOIN booking_slots bs ON b.id = bs.booking_id
    WHERE b.status IN ('CONFIRMED', 'COMPLETED')
"""
print("Fetching booking data...")
data = pd.read_sql(query, engine)

if data.empty:
    print("Warning: No booking data found in the database! The model cannot be trained.")
    exit(1)

print(f"Loaded {len(data)} booking records.")

# 3. Make a 'user-item' matrix
# rows = users, columns = turfs, values = count of slots booked
print("Processing data into turf-user matrix...")
turf_user = data.pivot_table(index="turf_id", columns="user_id",
                             values="slot_id", aggfunc="count").fillna(0)

print(f"Matrix shape: {turf_user.shape} (Turfs x Users)")

# 4. Train the Machine Learning Model
print("Training the NearestNeighbors model...")
model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(turf_user)

# 5. Save the trained model and the matrix for the API to use
print("Saving model to model.pkl and turf_user.pkl...")
joblib.dump(model, "model.pkl")
joblib.dump(turf_user, "turf_user.pkl")

print("Success! Model trained and saved. Phase 1 ready.")
