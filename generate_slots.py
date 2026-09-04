import datetime
from sqlalchemy import create_engine, text

import os
db_url = os.getenv("DB_URL", "mysql+pymysql://root@localhost:3306/buffturf_db")
engine = create_engine(db_url)

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
dates_to_seed = [today, tomorrow]

# Business hours 9 AM to 9 PM
hours = list(range(9, 21))

with engine.connect() as conn:
    # 1. Fetch all turf IDs
    turfs = [row[0] for row in conn.execute(text("SELECT id FROM turfs")).fetchall()]
    
    slots_inserted = 0
    for t_id in turfs:
        for d in dates_to_seed:
            for h in hours:
                start_time = datetime.time(hour=h, minute=0, second=0).isoformat()
                end_time = datetime.time(hour=h+1, minute=0, second=0).isoformat()
                
                # Check if slot already exists
                existing = conn.execute(
                    text("SELECT id FROM slots WHERE turf_id = :tid AND slot_date = :sdate AND start_time = :stime"),
                    {"tid": t_id, "sdate": d.isoformat(), "stime": start_time}
                ).fetchone()
                
                if not existing:
                    conn.execute(
                        text("""
                            INSERT INTO slots (turf_id, slot_date, start_time, end_time, is_available)
                            VALUES (:tid, :sdate, :stime, :etime, 1)
                        """),
                        {"tid": t_id, "sdate": d.isoformat(), "stime": start_time, "etime": end_time}
                    )
                    slots_inserted += 1

    conn.commit()
    print(f"Successfully generated {slots_inserted} new slots for today and tomorrow!")
