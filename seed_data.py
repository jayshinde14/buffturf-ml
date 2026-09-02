import random
import uuid
import datetime
from sqlalchemy import create_engine, text

print("Connecting to DB...")
engine = create_engine('mysql+pymysql://root:hpvictus@localhost:3306/buffturf_db')

with engine.connect() as conn:
    # 1. Fetch existing IDs
    users = [row[0] for row in conn.execute(text("SELECT id FROM users")).fetchall()]
    turfs = [row[0] for row in conn.execute(text("SELECT id FROM turfs")).fetchall()]
    slots = [row[0] for row in conn.execute(text("SELECT id FROM slots")).fetchall()]
    
    print(f"Found {len(users)} users, {len(turfs)} turfs, {len(slots)} slots")
    
    if not users or not turfs:
        print("Need at least 1 user and 1 turf.")
        exit()
        
    print("Generating 200 random bookings for better ML training...")
    # Generate 200 bookings
    for i in range(200):
        u_id = random.choice(users)
        t_id = random.choice(turfs)
        b_code = "DUMMY-" + str(uuid.uuid4())[:8].upper()
        b_date = datetime.date.today().isoformat()
        
        # Insert into bookings
        conn.execute(
            text("""
                INSERT INTO bookings (user_id, turf_id, booking_date, booking_code, status, created_at, amount_paid)
                VALUES (:uid, :tid, :bdate, :bcode, 'COMPLETED', NOW(), 500.0)
            """),
            {"uid": u_id, "tid": t_id, "bdate": b_date, "bcode": b_code}
        )
        
        # Get the inserted booking ID
        booking_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        
        turf_slots = [row[0] for row in conn.execute(
            text("SELECT id FROM slots WHERE turf_id = :tid"), {"tid": t_id}
        ).fetchall()]

        if not turf_slots:
            continue
            
        # Insert 1-3 slots for this booking
        num_slots = random.randint(1, 3)
        chosen_slots = random.sample(turf_slots, min(num_slots, len(turf_slots)))
        
        for s_id in chosen_slots:
            conn.execute(
                text("INSERT INTO booking_slots (booking_id, slot_id) VALUES (:bid, :sid)"),
                {"bid": booking_id, "sid": s_id}
            )
            
    conn.commit()
    print("Dummy data inserted successfully!")
