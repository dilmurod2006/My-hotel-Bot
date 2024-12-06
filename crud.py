import sqlite3
from datetime import datetime


# Database bilan ulanishni ta'minlash uchun funksiya
def databse_ulash():
    """
    Bu funksiya ma'lumotlar bazasiga ulanishni ta'minlaydi 
    va con (ulanish obyektini) va cur (kursor obyektini) qaytaradi.
    Kursor orqali SQL so'rovlarini yuboramiz.
    """
    # database.db nomli SQLite ma'lumotlar bazasiga ulanish
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    return con, cur


# Admin qo'shish funksiyasi
def create_admin(full_name, telegram_id):
    """
     Bu funksiya admins jadvaliga yangi admin qo'shish uchun ishlatiladi. 
     full_name (adminning to'liq ismi) va telegram_id (adminning Telegram IDsi) 
     qiymatlari parametr sifatida olinadi.
     So'rovni bajarishdan so'ng o'zgarishlar con.commit() bilan saqlanadi.
     """
    try:
        # Databasega ulanish
        con, cur = databse_ulash()
        
        # Adminni 'admins' jadvaliga qo'shish
        cur.execute("""
        INSERT INTO admins (full_name, telegram_id)
        VALUES (?, ?)
        """, (full_name, telegram_id))  # 'full_name' va 'telegram_id' qiymatlarini jadvalga kiritish
        
        # O'zgarishlarni bazaga saqlash
        con.commit()
        
        # Yangi admin muvaffaqiyatli qo'shildi degan xabarni ko'rsatish
        # print(f"Admin '{full_name}' muvaffaqiyatli qo'shildi.")
    except sqlite3.Error as e:
        # Xato yuz berishi mumkin, shuning uchun xatolikni qayd qilish
        print(f"Xatolik yuz berdi: {e}")
    finally:
        # Ma'lumotlar bazasi bilan aloqani yopish
        con.close()


# Adminlarni ko'rish funksiyasi
# Bu funksiya barcha adminlarni bazadan olib, ekranda ko'rsatadi
def get_all_admins():
    """
    Bu funksiya barcha adminlarni bazadan olib, 
    ularni ekranda ko'rsatadi. Agar adminlar mavjud bo'lsa,
    ularning ID va ismlari chiqariladi.
    Agar adminlar mavjud bo'lmasa, xabar beradi.
    """
    try:
        # Databasega ulanish
        con, cur = databse_ulash()
        
        # Adminlarni 'admins' jadvalidan tanlash
        cur.execute("SELECT id, full_name FROM admins")
        admins = cur.fetchall()  # Barcha adminlar ma'lumotlarini olish
        
        # Agar adminlar mavjud bo'lsa
        if admins:
            # print("Hozirgi adminlar ro'yxati:")
            # Har bir adminning ID va ismini chiqarish
            for admin in admins:
                print(f"ID: {admin[0]}, Ismi: {admin[1]}")
            return admins  # Adminlarning ID va ismlari ro'yxatini qaytarish
        else:
            # Agar adminlar mavjud bo'lmasa
            print("Hech qanday admin topilmadi.")
            return []  # Hech qanday admin bo'lmasa, bo'sh ro'yxat qaytarish
    except sqlite3.Error as e:
        # Xato yuz berishi mumkin, shuning uchun xatolikni qayd qilish
        print(f"Xatolik yuz berdi: {e}")
        return []  # Xatolik bo'lsa, bo'sh ro'yxat qaytarish
    finally:
        # Ma'lumotlar bazasi bilan aloqani yopish
        con.close()


# Adminni o'chirish funksiyasi
# Bu funksiya berilgan admin ID bo'yicha adminni bazadan o'chirish uchun ishlatiladi
def delete_admin(admin_id):
    """
    Bu funksiya berilgan admin ID'siga asosan adminni bazadan o'chiradi.
    Agar admin o'chirilsa, muvaffaqiyatli xabar beradi; aks holda,
    admin topilmaganini bildiradi.
    """
    try:
        # Databasega ulanish
        con, cur = databse_ulash()
        
        # Adminni 'admins' jadvalidan o'chirish
        cur.execute("DELETE FROM admins WHERE id = ?", (admin_id,))
        
        # Agar o'chirish muvaffaqiyatli bo'lsa
        if cur.rowcount > 0:
            return f"Admin ID: {admin_id} muvaffaqiyatli o'chirildi."
        else:
            # Agar admin topilmasa
            return f"Admin ID: {admin_id} topilmadi."
        
        # O'zgarishlarni bazaga saqlash
        con.commit()
    except sqlite3.Error as e:
        # Xato yuz berishi mumkin, shuning uchun xatolikni qayd qilish
        print(f"Xatolik yuz berdi: {e}")
    finally:
        # Ma'lumotlar bazasi bilan aloqani yopish
        con.close()


# Sinovdan o'tkazish
# Yangi admin qo'shish
# create_admin("Abdulla Normatov", 123456789)

# Adminni o'chirish
# delete_admin(1)





# Xona turi qo'shish uchun funksiya
# Ushbu funksiya yangi xona turini 'xonaturi' jadvaliga qo'shish uchun ishlatiladi.
# Foydalanuvchi berilgan 'xona_turi' qiymatini jadvalga kiritadi va muvaffaqiyatli qo'shilganligi haqida xabar qaytaradi.
def xona_turi_qushish(xona_turi: str) -> str:
    """
    Bu funksiya xona_turi nomli yangi xona turini xonaturi jadvaliga qo'shish uchun ishlatiladi.
    xona_turi - foydalanuvchi tomonidan berilgan xona turi nomi bo'lib, 
    bu qiymat jadvalga kiritiladi.
    Funksiya bajarilgach, muvaffaqiyatli qo'shilganligi haqida xabar qaytariladi.   
    """
    # Databasega ulanish
    con, cur = databse_ulash()
    
    # 'xonaturi' jadvaliga yangi xona turini qo'shish
    cur.execute("""
    INSERT INTO xonaturi (xona_turi)
    VALUES (?)
    """, (xona_turi,))  # 'xona_turi' qiymati jadvalga kiritiladi
    
    # O'zgarishlarni bazaga saqlash
    con.commit()
    
    # Database bilan aloqani yopish
    con.close()
    
    # Muvaffaqiyatli qo'shilgan xona turi haqida xabar qaytarish
    return f"Xona turi: {xona_turi} muvaffaqiyatli qo'shildi!"


# Xona turlari ro'yxati
# Bu ro'yxatdagi barcha xona turlari birma-bir qo'shiladi
# xona_turlari = ["standart", "premium", "delux", "royal", "vip", "lux"]

# Har bir xona turini jadvalga qo'shish
# for xona_turi in xona_turlari:
    # Xona turini qo'shish
    # natija = xona_turi_qushish(xona_turi)
    # Muvaffaqiyatli qo'shilganligini ekranda ko'rsatish
    # print(natija)





# Xonalar qo'shish uchun funksiya
# Ushbu funksiya 'xonalar' jadvaliga yangi xona qo'shish uchun ishlatiladi.
# Foydalanuvchi xona raqami, xona turi, xona haqida ma'lumot va narxni kiritadi.
# Xona bandligi doim bo'sh (0) bo'ladi, shuning uchun band_xona qiymati kiritilmasa, default 0 bo'ladi.

def xona_qushish(xona_raqami: int, xona_turi_id: int, xona_haqida: str, price: int) -> str:
    """
    Xona qo'shish funksiyasi
    :param xona_raqami: Xonaning unik raqami
    :param xona_turi_id: Xona turiga mos ID (foreign key)
    :param xona_haqida: Xona haqida qisqacha ma'lumot
    :param price: Xonaning narxi
    :return: Xona muvaffaqiyatli qo'shilganligi haqida xabar
    """
    
    # Databasega ulanish
    con, cur = databse_ulash()

    try:
        # Yangi xona qo'shish
        cur.execute("""
        INSERT INTO xonalar (xona_raqami, xona_turi_id, xona_haqida, price, band_xona)
        VALUES (?, ?, ?, ?, ?)
        """, (xona_raqami, xona_turi_id, xona_haqida, price, 0))  # band_xona doimo 0 bo'ladi (bo'sh)

        # O'zgarishlarni bazaga saqlash
        con.commit()
        
        # Muvaffaqiyatli qo'shilganligi haqida xabar qaytarish
        return f"Xona raqami {xona_raqami} muvaffaqiyatli qo'shildi!"

    except sqlite3.Error as e:
        # Xatolik yuz berganda
        return f"Xatolik yuz berdi: {e}"
    
    finally:
        # Database bilan aloqani yopish
        con.close()


# Sinov uchun: yangi xonalar qo'shish
# Misol uchun, xona raqami 101, tur 1 (premium), xona haqida ma'lumot, narx va bandligi (bo'sh) qo'shiladi.
# print(xona_qushish(101, 1, "Premium xona, ikki kishilik", 200))
# print(xona_qushish(102, 2, "Lux xona, katta to'plam", 500))




# Xona turiga qarab bo'sh xonalarni topish funksiyasi
# Ushbu funksiya berilgan xona turi bo'yicha bo'sh xonalarni topish uchun ishlatiladi.
# Funksiya xonalar jadvalidan turga mos bo'sh xonalarni chiqaradi va ular haqida ma'lumotlarni qaytaradi.

def bush_xonalar_topish(xona_turi_id):
    """
    Xona turiga qarab bo'sh xonalarni topish funksiyasi
    :param xona_turi_id: Xona turi ID (foreign key)
    :return: Xona turi va unga mos bo'sh xonalar ro'yxati yoki xabar
    """
    
    # Databasega ulanish
    con, cur = databse_ulash()

    # 1. Xona turi haqida ma'lumot olish (xona_turi nomini olish)
    cur.execute(""" 
    SELECT xona_turi
    FROM xonaturi
    WHERE id = ? 
    """, (xona_turi_id,))
    
    # Xona turi mavjud bo'lmasa, xatolik haqida xabar qaytarish
    xona_turi = cur.fetchone()
    if not xona_turi:
        con.close()
        return {"message": f"Xona turi ID {xona_turi_id} topilmadi."}
    
    # Xona turi nomini olish
    xona_turi = xona_turi[0]

    # 2. Bo'sh xonalarni olish
    cur.execute("""
    SELECT x.xona_raqami, t.xona_turi, x.xona_haqida, x.price
    FROM xonalar x
    JOIN xonaturi t ON x.xona_turi_id = t.id
    WHERE x.xona_turi_id = ? AND x.band_xona = 0  -- band_xona = 0 bo'lsa, xona bo'sh
    """, (xona_turi_id,))

    # 3. Xonalar natijalarini olish
    xonalar = cur.fetchall()
    con.close()

    # Agar bo'sh xonalar mavjud bo'lmasa
    if not xonalar:
        return {"message": f"{xona_turi} turiga mos bo'sh xonalar topilmadi."}

    # 4. Xonalar ro'yxatini formatlash va qaytarish
    return {
        "xona_turi": xona_turi,  # Xona turi nomini ko'rsatish
        "bush_xonalar": [
            {"room_id": xona[0], "xona_turi": xona[1], "xona_haqida": xona[2], "price": xona[3]} 
            for xona in xonalar  # Har bir bo'sh xonaning ma'lumotlarini formatlash
        ],
        "message": f"{xona_turi} turiga mos bo'sh xonalar ro'yxati!"  # Muvaffaqiyatli xabar
    }








# Xona buyurtmasi berish funksiyasi
# Ushbu funksiya foydalanuvchidan buyurtma olish va uni `user_orders` jadvaliga saqlash uchun ishlatiladi.
# Funksiya foydalanuvchining ma'lumotlarini, xonani, va qolish vaqtini kiritib buyurtmani tizimga qo'shadi.

def xona_buyurtma_berish(full_name, tugilgan_yili, jinsi, passport_seriya, passport_yili, phone_number, xona_raqami, start_date, end_date):
    """
    Foydalanuvchi uchun xona buyurtmasini tizimga qo'shish funksiyasi.
    :param full_name: Foydalanuvchining to'liq ismi
    :param tugilgan_yili: Foydalanuvchining tug'ilgan yili
    :param jinsi: Foydalanuvchining jinsi (0 - ayol, 1 - erkak)
    :param passport_seriya: Foydalanuvchining pasport seriyasi
    :param passport_yili: Foydalanuvchining pasport berilgan yili
    :param phone_number: Foydalanuvchining telefon raqami
    :param xona_raqami: Foydalanuvchi qaysi xonada joylashgan
    :param start_date: Xonada qolish boshlanish sanasi
    :param end_date: Xonada qolish tugash sanasi
    :return: Buyurtma muvaffaqiyatli qo'shilganligi haqida xabar
    """
    con, cur = databse_ulash()  # Ma'lumotlar bazasiga ulanish
    
    try:
        # 1. Buyurtmani `user_orders` jadvaliga kiritish
        cur.execute("""
        INSERT INTO user_orders (full_name, tugilgan_yili, jinsi, passport_seriya, passport_yili, phone_number, xona_raqami, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name, tugilgan_yili, jinsi, passport_seriya, passport_yili, phone_number, xona_raqami, start_date, end_date))
        
        # 2. O'zgarishlarni bazaga saqlash
        con.commit()

        # 3. Xonada qolish vaqtining tugashiga vaqtning aniq formatini olish
        start_date = datetime.strptime(start_date, "%d.%m.%Y %H:%M")  # Sanani formatlash
        end_date = datetime.strptime(end_date, "%d.%m.%Y %H:%M")  # Sanani formatlash
        
        # 4. Xona bandligini tekshirish va yangilash
        cur.execute("""
        UPDATE xonalar
        SET band_xona = 1  -- Xona band bo'ladi
        WHERE xona_raqami = ? AND band_xona = 0  -- Faqat bo'sh xonalar
        """, (xona_raqami,))

        # O'zgarishlarni saqlash
        con.commit()
        
        con.close()
        return {"message": "Buyurtma muvaffaqiyatli qabul qilindi!"}
    
    except Exception as e:
        con.close()  # Baxtsiz holatda bog'lanishni yopish
        return {"message": f"Xatolik yuz berdi: {str(e)}"}

# Sinov uchun misol chaqirish:
# print(xona_buyurtma_berish("Amonov Dilmurod", "23.11.2006", 1, "AD12567", "2023", "+998901234567", 1, "06.12.2024 12:00", "08.12.2024 18:00"))






# Xona turlarini olish funksiyasi
def get_all_room_types():
    """
    Ushbu funksiya bazadagi barcha xona turlarini olish uchun ishlatiladi.
    Xona turlari jadvalidan (xonaturi) barcha ma'lumotlarni olish va 
    ularni ekranga chiqarish yoki ro'yxat sifatida qaytarish.
    """
    try:
        # Databasega ulanish
        con, cur = databse_ulash()
        
        # Xona turlarini olish uchun SQL so'rovini bajarish
        cur.execute("SELECT id, xona_turi FROM xonaturi")
        room_types = cur.fetchall()  # Barcha natijalarni olish
        
        # Agar xona turlari mavjud bo'lsa, ularni ekranga chiqarish
        if room_types:
            print("Hozirgi xona turlari:")
            for room in room_types:
                print(f"ID: {room[0]}, Xona turi: {room[1]}")  # Har bir xona turi haqida ma'lumot chiqariladi
            return room_types  # Xona turlari ro'yxatini qaytaradi (id va xona_turi)
        else:
            print("Hech qanday xona turi topilmadi.")  # Agar xona turi topilmasa
            return []  # Bo'sh ro'yxat qaytariladi
    except sqlite3.Error as e:
        # Xatolik yuz berganda
        print(f"Xatolik yuz berdi: {e}")
        return []  # Xatolik yuz berganida bo'sh ro'yxat qaytariladi
    finally:
        # Ma'lumotlar bazasi bilan ishlash tugagach ulanishni yopish
        con.close()

# # Sinovdan o'tkazish
# room_types = get_all_room_types()
# print("Xona turlari: ", room_types)
























# Admin uchun user_orders jadvalidan ma'lumotlarni formatda qaytarish funksiyasi
def get_user_orders_for_admin():
    """
    Ushbu funksiya, admin uchun barcha foydalanuvchilarning buyurtmalarini va ularning xonalariga oid ma'lumotlarni olishni ta'minlaydi.
    Ma'lumotlar user_orders, xonalar, va xonaturi jadvalidan birlashtiriladi va admin uchun o'qilishi oson formatda qaytariladi.
    """
    con, cur = databse_ulash()  # Databasega ulanish

    try:
        # SQL so'rov: user_orders, xonalar va xonaturi jadvalini birlashtirib ma'lumotlarni olish
        cur.execute("""
        SELECT 
            u.id,  -- Buyurtma ID
            u.full_name,  -- Foydalanuvchining to'liq ismi
            u.tugilgan_yili,  -- Tug'ilgan yili
            CASE u.jinsi WHEN 1 THEN 'Erkak' ELSE 'Ayol' END AS jinsi,  -- Jinsi (0 - Ayol, 1 - Erkak)
            u.passport_seriya,  -- Pasport seriyasi
            u.passport_yili,  -- Pasport berilgan yili
            x.xona_turi AS xona_turi,  -- Xona turi (agar mavjud bo'lsa)
            u.created_at  -- Buyurtma yaratilgan vaqt
        FROM user_orders u
        LEFT JOIN xonalar xh ON u.xona_raqami = xh.xona_raqami  -- Xonalar bilan bog'lanish
        LEFT JOIN xonaturi x ON xh.xona_turi_id = x.id;  -- Xona turini olish
        """)

        # Ma'lumotlarni olish
        orders = cur.fetchall()

        # Agar buyurtmalar mavjud bo'lsa, ularni formatlash
        formatted_orders = []
        for order in orders:
            formatted_orders.append({
                "ID": order[0],  # Buyurtma ID
                "Ism-familiya": order[1],  # Foydalanuvchining to'liq ismi
                "Tug'ilgan yili": order[2],  # Foydalanuvchining tug'ilgan yili
                "Jinsi": order[3],  # Foydalanuvchining jinsi (Erkak yoki Ayol)
                "Passport seriyasi": order[4],  # Pasport seriyasi
                "Passport yili": order[5],  # Pasport berilgan yili
                "Xona turi": order[6] if order[6] is not None else "N/A",  # Xona turi (Agar mavjud bo'lmasa, "N/A" qaytariladi)
                "Yaratilgan vaqti": order[7]  # Buyurtma yaratilgan vaqti
            })

        return formatted_orders  # Formatlangan buyurtmalar ro'yxatini qaytaradi

    except sqlite3.Error as e:
        # Xatolik yuz berganda, xatolikni konsolga chiqarish
        print(f"Xatolik yuz berdi: {e}")
        return []  # Xatolik yuz berganida bo'sh ro'yxat qaytariladi
    
    finally:
        # Ma'lumotlar bazasiga bo'lgan ulanishni yopish
        con.close()

# natija = get_user_orders_for_admin()
# print(natija)




# Passport seriyasi orqali buyurtmani olish funksiyasi
def get_order_by_passport(passport_seriya):
    """
    Ushbu funksiya, foydalanuvchining passport seriyasi bo'yicha buyurtma ma'lumotlarini olishni ta'minlaydi.
    Passport seriyasi orqali buyurtma mavjudligini tekshirib, agar topilsa, foydalanuvchi haqidagi barcha ma'lumotlarni qaytaradi.
    Agar buyurtma topilmasa, foydalanuvchiga ma'lumot yo'qligi haqida xabar beradi.
    """
    con, cur = databse_ulash()  # Databasega ulanish

    try:
        # SQL so'rov: user_orders, xonalar va xonaturi jadvalini birlashtirib, passport_seriya orqali buyurtma topish
        cur.execute("""
        SELECT 
            u.id,  -- Buyurtma ID
            u.full_name,  -- Foydalanuvchining to'liq ismi
            u.tugilgan_yili,  -- Tug'ilgan yili
            CASE u.jinsi WHEN 1 THEN 'Erkak' ELSE 'Ayol' END AS jinsi,  -- Jinsi (0 - Ayol, 1 - Erkak)
            u.passport_seriya,  -- Pasport seriyasi
            u.passport_yili,  -- Pasport berilgan yili
            x.xona_turi AS xona_turi,  -- Xona turi (agar mavjud bo'lsa)
            u.created_at  -- Buyurtma yaratilgan vaqt
        FROM user_orders u
        LEFT JOIN xonalar xh ON u.xona_raqami = xh.xona_raqami  -- Xonalar bilan bog'lanish
        LEFT JOIN xonaturi x ON xh.xona_turi_id = x.id  -- Xona turini olish
        WHERE u.passport_seriya = ?;  -- Foydalanuvchining passport seriyasiga mos buyurtmani tanlash
        """, (passport_seriya,))

        # Ma'lumotlarni olish (faqat bitta buyurtma, chunki passport_seriya unikal bo'lishi kerak)
        order = cur.fetchone()

        # Agar buyurtma topilmasa
        if not order:
            return f"Passport seriyasi '{passport_seriya}' bo'yicha hech qanday buyurtma topilmadi."

        # Formatlangan natija
        formatted_order = {
            "ID": order[0],  # Buyurtma ID
            "Ism-familiya": order[1],  # Foydalanuvchining to'liq ismi
            "Tug'ilgan yili": order[2],  # Foydalanuvchining tug'ilgan yili
            "Jinsi": order[3],  # Foydalanuvchining jinsi (Erkak yoki Ayol)
            "Passport seriyasi": order[4],  # Pasport seriyasi
            "Passport yili": order[5],  # Pasport berilgan yili
            "Xona turi": order[6] if order[6] is not None else "N/A",  # Xona turi (Agar mavjud bo'lmasa, "N/A" qaytariladi)
            "Yaratilgan vaqti": order[7]  # Buyurtma yaratilgan vaqti
        }

        return formatted_order  # Formatlangan buyurtma ma'lumotini qaytarish

    except sqlite3.Error as e:
        # Xatolik yuz berganda, xatolikni konsolga chiqarish
        print(f"Xatolik yuz berdi: {e}")
        return None  # Xatolik yuz berganida None qaytariladi

    finally:
        # Ma'lumotlar bazasiga bo'lgan ulanishni yopish
        con.close()

# Sinovdan o'tkazish
# natija = get_order_by_passport("AA1233334567")
# print(natija)

# Bo'sh xonalarni olish funksiyasi
def get_available_rooms(room_type_id):
    try:
        con, cur = databse_ulash()
        cur.execute("""
            SELECT xona_raqami, narx, tavsif
            FROM xonalar
            WHERE xona_turi_id = ? AND band_xona = 0
        """, (room_type_id,))
        available_rooms = cur.fetchall()
        con.close()
        return available_rooms
    except sqlite3.Error as e:
        print(f"Xatolik: {e}")
        return []