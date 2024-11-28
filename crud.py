import sqlite3


# databse ulash
def databse_ulash():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    return con, cur




# xonalar turini qo'shish uchun funksiya adminstator uchun
def xona_turi_qushish(xona_turi:str) -> str:
    con,cur = databse_ulash()
    cur.execute("""
    INSERT INTO xonaturi (xona_turi)
    VALUES (?)
    """, (xona_turi,))
    con.commit()
    con.close()
    return f"Xona turi: {xona_turi} muvaffaqiyatli qo'shildi!"

# xona_turlari = ["standart", "premium", "delux", "royal", "vip", "lux"]



# for choynakning_qopqogi in xona_turlari:
#     natija =xona_turi_qushish(choynakning_qopqogi) 
#     print(natija)




# xonalar qo'shish funksiyasi
def xonalar_qushish(room_id:int, xona_turi_id:int, band_xona:bool) -> str:
    con,cur = databse_ulash()
    cur.execute("""
    INSERT INTO xonalar (room_id, xona_turi_id,band_xona)
    VALUES (?, ?, ?)
    """, (room_id, xona_turi_id,band_xona))
    con.commit()
    con.close()
    return f"{room_id} Xona muvaffaqiyatli qo'shildi!"


# xonalar_data = [
#     {"room_id": 230, "xona_turi_id": 1, "band_xona": False},
#     {"room_id": 231, "xona_turi_id": 2,"band_xona": False},
#     {"room_id":227, "xona_turi_id": 5,"band_xona": False},
# ]

# # for sikli orqali ma'lumotlar qo'shish
# for malumot in xonalar_data:
#     natija = xonalar_qushish(malumot["room_id"], malumot["xona_turi_id"], malumot["band_xona"])
#     print(natija)



# xona turiga qarab barcha bo'sh xonalarni chiqarib beradigan funksiya
def bush_xonalar_topish(xona_turi):
    con, cur = databse_ulash()

    cur.execute("""
    SELECT x.room_id, t.xona_turi
    FROM xonalar x
    JOIN xonaturi t ON x.xona_turi_id = t.id
    WHERE t.xona_turi = ? AND x.band_xona = 0
    """, (xona_turi,))

    # Natijalarni olish
    xonalar = cur.fetchall()
    con.close()

    if not xonalar:
        return {"message": f"{xona_turi} turiga mos bo'sh xonalar topilmadi."}

    # Xonalarni formatlash
    return {
        "xona_turi": xona_turi,
        "bush_xonalar": [{"room_id": xona[0], "xona_turi": xona[1]} for xona in xonalar],
        "message": f"{xona_turi} turiga mos bo'sh xonalar ro'yxati!"
    }




# xona buyurtma qilish uchun funksiya
def xona_buyurtma_qilish(full_name, tugilgan_yili, jinsi, passport_seriya, passport_yili, xona_id):
    con, cur = databse_ulash()

    # Xona bandlik holatini tekshirish
    cur.execute("SELECT band_xona FROM xonalar WHERE room_id = ?", (xona_id,))
    xona = cur.fetchone()

    if xona is None:
        con.close()
        return {
            "error": f"Xona ID {xona_id} mavjud emas!"
        }

    if xona[0]:  # Agar xona band bo'lsa
        con.close()
        return {
            "error": f"Xona ID {xona_id} band. Iltimos, boshqa xona tanlang!"
        }

    # Xona bo'sh bo'lsa, buyurtma qo'shiladi
    cur.execute("""
    INSERT INTO user_orders (full_name, tugilgan_yili, jinsi, passport_seriya, passport_yili, xona_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (full_name, tugilgan_yili, jinsi, passport_seriya, passport_yili, xona_id))

    # Xonani band deb belgilash
    cur.execute("UPDATE xonalar SET band_xona = 1 WHERE room_id = ?", (xona_id,))

    con.commit()
    con.close()

    # Jinsni matn ko'rinishiga o'zgartirish
    jinsi_text = "Erkak" if jinsi else "Ayol"

    return {
        "user_data": {
            "full_name": full_name,
            "tugilgan_yili": tugilgan_yili,
            "jinsi": jinsi_text,
            "passport_seriya": passport_seriya,
            "passport_yili": passport_yili,
            "xona_id": xona_id
        },
        "message": "Xurmatli foydalanuvchi, sizning buyurtmangiz muvaffaqiyatli qabul qilindi!"
    }




# test qilish

# user_data = {
#     "full_name": "Shodmon",
#     "tugilgan_yili": "20.03.2005",
#     "jinsi": True,
#     "passport_seriya": "AA12345346",
#     "passport_yili": "2023",
#     "xona_id": 231
# }

# # buyurtma_qabul_qilindi = xona_buyurtma_qilish(**user_data)

# buyurtma_qabul_qilindi = xona_buyurtma_qilish(
#     user_data["full_name"], 
#     user_data["tugilgan_yili"], 
#     user_data["jinsi"], 
#     user_data["passport_seriya"], 
#     user_data["passport_yili"], 
#     user_data["xona_id"]
# )

# print(buyurtma_qabul_qilindi)



# test qilish tugadi





























# Admin uchun user_orders jadvalidan ma'lumotlarni formatda qaytarish
def get_user_orders_for_admin():
    con, cur = databse_ulash()
    # SQL so'rov: user_orders, xonalar va xonaturi jadvalini birlashtirish
    cur.execute("""
    SELECT 
        u.id,
        u.full_name,
        u.tugilgan_yili,
        CASE u.jinsi WHEN 1 THEN 'Erkak' ELSE 'Ayol' END AS jinsi,
        u.passport_seriya,
        u.passport_yili,
        x.xona_turi AS xona_turi,
        u.created_at
    FROM user_orders u
    LEFT JOIN xonalar xh ON u.xona_id = xh.room_id
    LEFT JOIN xonaturi x ON xh.xona_turi_id = x.id;
    """)

    # Ma'lumotlarni olish
    orders = cur.fetchall()

    # Ma'lumotlarni formatlash
    formatted_orders = []
    for order in orders:
        formatted_orders.append({
            "ID": order[0],
            "Ism-familiya": order[1],
            "Tug'ilgan yili": order[2],
            "Jinsi": order[3],
            "Passport seriyasi": order[4],
            "Passport yili": order[5],
            "Xona turi": order[6] if order[6] is not None else "N/A",
            "Yaratilgan vaqti": order[7]
        })

    con.close()
    return formatted_orders


# natija = get_user_orders_for_admin()
# print(natija)



# Passport seriyasi orqali buyurtmani olish
def get_order_by_passport(passport_seriya):
    con, cur = databse_ulash()

    # SQL so'rov: user_orders, xonalar va xonaturi jadvalini birlashtirish
    cur.execute("""
    SELECT 
        u.id,
        u.full_name,
        u.tugilgan_yili,
        CASE u.jinsi WHEN 1 THEN 'Erkak' ELSE 'Ayol' END AS jinsi,
        u.passport_seriya,
        u.passport_yili,
        x.xona_turi AS xona_turi,
        u.created_at
    FROM user_orders u
    LEFT JOIN xonalar xh ON u.xona_id = xh.room_id
    LEFT JOIN xonaturi x ON xh.xona_turi_id = x.id
    WHERE u.passport_seriya = ?;
    """, (passport_seriya,))

    # Ma'lumotlarni olish
    order = cur.fetchone()
    con.close()

    # Agar buyurtma topilmasa
    if not order:
        return f"Passport seriyasi '{passport_seriya}' bo'yicha hech qanday buyurtma topilmadi."

    # Formatlangan natija
    formatted_order = {
        "ID": order[0],
        "Ism-familiya": order[1],
        "Tug'ilgan yili": order[2],
        "Jinsi": order[3],
        "Passport seriyasi": order[4],
        "Passport yili": order[5],
        "Xona turi": order[6] if order[6] is not None else "N/A",
        "Yaratilgan vaqti": order[7]
    }

    return formatted_order

# natija = get_order_by_passport("AA1233225346")
# print(natija)