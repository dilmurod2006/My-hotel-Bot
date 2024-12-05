import sqlite3

# Databaza yaratish funksiyasi
def create_frame_databse():
    # database.db nomli SQLite database'ga ulanish
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # 1. `user_orders` jadvali yaratish
    # Ushbu jadval foydalanuvchilarning buyurtmalarini saqlaydi
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_orders (
        id INTEGER PRIMARY KEY,  -- Buyurtmaning unikal identifikatori
        full_name TEXT,  -- Foydalanuvchining to'liq ismi
        tugilgan_yili TEXT,  -- Foydalanuvchining tug'ilgan yili
        jinsi INTEGER,  -- Foydalanuvchining jinsi (INTEGER: 0 - ayol, 1 - erkak)
        passport_seriya TEXT,  -- Foydalanuvchining pasport seriyasi
        passport_yili TEXT,  -- Foydalanuvchining pasport berilgan yili
        phone_number TEXT,  -- Foydalanuvchining telefon raqami
        xona_raqami INTEGER,  -- Foydalanuvchi qaysi xonada joylashgan (foreign key)
        start_date DATETIME NOT NULL,  -- Xonada qolish boshlanish sanasi
        end_date DATETIME NOT NULL,  -- Xonada qolish tugash sanasi
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Buyurtma yaratilgan sana (default: hozirgi vaqt)
        FOREIGN KEY (xona_raqami) REFERENCES xonalar (xona_raqami)  -- `xona_raqami` boshqa jadvaldan (xonalar) olingan foreign key
    );
    """)

    # 2. `xonaturi` jadvali yaratish
    # Bu jadval xonalar turlarini saqlaydi (masalan, bir yotoqxonali, ikki yotoqxonali)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS xonaturi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unikal identifikator (avtomatik o'suvchi)
        xona_turi TEXT  -- Xona turining nomi (masalan: "Yotoqxona", "Deluxe")
    );
    """)

    # 3. `xonalar` jadvali yaratish
    # Bu jadvaldagi xonalar ma'lumotlarini saqlaydi, xonalar narxi va holatini belgilaydi
    cur.execute("""
    CREATE TABLE IF NOT EXISTS xonalar (
        xona_raqami INTEGER NOT NULL PRIMARY KEY,  -- Xona raqami (unikal)
        xona_turi_id INTEGER NOT NULL,  -- Xona turi (foreign key)
        xona_haqida TEXT,  -- Xona haqida qisqacha ma'lumot
        price INTEGER NOT NULL,  -- Xonaning narxi
        band_xona INTEGER DEFAULT 0,  -- Xona bandligi (0 - bo'sh, 1 - band)
        FOREIGN KEY (xona_turi_id) REFERENCES xonaturi (id)  -- `xona_turi_id` foreign key
    );
    """)

    # 4. `admins` jadvali yaratish
    # Ushbu jadvalda tizim administratorlarining ma'lumotlari saqlanadi
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Administratorning unikal identifikatori
        full_name TEXT,  -- Administratorning to'liq ismi
        telegram_id INTEGER NOT NULL  -- Administratorning Telegram IDsi
    );
    """)

    # O'zgarishlarni bazaga saqlash
    con.commit()
    # Baza bilan aloqani to'xtatish
    con.close()

# Funksiyani chaqirish
create_frame_databse()
