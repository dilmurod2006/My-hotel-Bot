# sqlite3 modulini import qilish
import sqlite3



# databse yaratish 
def create_frame_databse():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # 1. `user_orders` jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_orders (
        id INTEGER PRIMARY KEY,
        full_name TEXT,
        tugilgan_yili TEXT,
        jinsi BOOLEAN,
        passport_seriya TEXT,
        passport_yili TEXT,
        phone_number TEXT,
        xona_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (xona_id) REFERENCES xonalar (room_id)
    );
    """)

    # 2. `xonaturi` jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS xonaturi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        xona_turi TEXT
    );
    """)

    # 3. `xonalar` jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS xonalar (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        xona_turi_id INTEGER NOT NULL,
        xona_haqida TEXT,
        band_xona BOOLEAN DEFAULT 0,
        FOREIGN KEY (xona_turi_id) REFERENCES xonaturi (id)
    );
    """)


    # 4. 'admins' jadvali
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        telegram_id BIGINTEGER NOT NULL
    );
"""
    )


    con.commit()
    con.close()


create_frame_databse()