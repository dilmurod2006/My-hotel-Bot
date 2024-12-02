import telebot
from telebot import types
from crud import (
    xona_turi_qushish,
    xonalar_qushish,
    xona_buyurtma_qilish,
    get_user_orders_for_admin,
    get_order_by_passport,
    bush_xonalar_topish,
    create_admin,
    delete_admin,
    get_all_admins,
    get_all_room_types
)

TOKEN = "7675610993:AAEZzNcQJpGWTOctlGx9cjbulGsvTkogv0g"
bot = telebot.TeleBot(TOKEN)

ADMINS = [1231232131,7054004046,5420071824]

text = """
Assalomu aleykum Xurmatli mijoz! Sizni botimizga tashrifingizdan bag'oyatda xursandmiz! 😇
"""

user_data = {}  # Dictionary to maintain user data

@bot.message_handler(commands=['start'])
def boshlash(message):
    """
    /start buyrug'iga javob beruvchi funksiya.
    """
    if message.chat.id in ADMINS:
        # Admin paneli uchun tugmalar
        tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tugma.add("Buyurtmani tekshirish 🔎","Barcha Buyurtmalar 📄")
        tugma.add("Xona turini qo'shish ➕","Xona qo'shish ➕")
        tugma.add("Sozlamalar ⚙️")

        bot.send_message(message.chat.id, "Admin paneliga xush kelibsiz!", reply_markup=tugma)
    else:
        # Oddiy foydalanuvchi uchun menyu
        tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tugma.add("Xona buyurtma qilish", "Mexmonhona haqida")
        bot.send_message(message.chat.id, text, reply_markup=tugma)

@bot.message_handler(content_types=['text'])
def tugmalarga_javob_berish(message):
    """
    Oddiy foydalanuvchi uchun tugmalarni boshqarish.
    """
    if message.text == "Xona buyurtma qilish":
        markup = types.InlineKeyboardMarkup()
        xona_turi = get_all_room_types()  # Xona turlari ro'yxatini olish
        if xona_turi:
            for xona in xona_turi:
                markup.add(types.InlineKeyboardButton(xona[1], callback_data=f"xona_{xona[0]}"))
            bot.send_message(message.chat.id, "Xona turini tanlang:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Hozircha hech qanday xona turi mavjud emas.")
    elif message.text == "Mexmonhona haqida":
        bot.send_message(message.chat.id, "Bu bot orqali mehmonxona haqida ma'lumot olishingiz va xonalarni buyurtma qilishingiz mumkin.")
    elif message.text == "Buyurtmani tekshirish 🔎":
        # Admin uchun passport seriyasi orqali buyurtma tekshirish
        bot.send_message(message.chat.id, "Pasport seriya va raqamini kiriting:")
        bot.register_next_step_handler(message, process_passport_input)
    elif message.text == "Barcha Buyurtmalar 📄":
        # Admin uchun buyurtmalarni ko'rsatish
        orders = get_user_orders_for_admin()
        response = ""
        if orders:
            for order in orders:
                response += f"""
ID: {order['ID']}
Ism-familiya: {order['Ism-familiya']}
Tug'ilgan yili: {order["Tug'ilgan yili"]}
Jinsi: {order['Jinsi']}
Passport seriyasi: {order['Passport seriyasi']}
Xona turi: {order['Xona turi']}
Yaratilgan vaqti: {order['Yaratilgan vaqti']}
"""

        else:
            response = "Hozircha hech qanday buyurtma mavjud emas."

        bot.send_message(message.chat.id, response)

    # xona turini qo'shish
    elif message.text == "Xona turini qo'shish ➕":
        # Xona turini qo'shish funksiyasiga kirish
        bot.send_message(message.chat.id, "Yangi xona turini kiriting:")
        bot.register_next_step_handler(message, process_xona_turi_input)
    
    # xona qo'shsish
    elif message.text == "Xona qo'shish ➕":
        # Xona qo'shish funksiyasiga kirish
        bot.send_message(message.chat.id, "Xona ID sini kiriting:")
        bot.register_next_step_handler(message, process_room_id_input)

    # sozlamalar
    elif "Sozlamalar ⚙️" == message.text:
        tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tugma.add("Admin qo'shish ➕", "Adminlar 📄")
        tugma.add("Admini o'chirish 🗑")
        bot.send_message(message.chat.id, "Sozlamalar bo'limi!", reply_markup=tugma)


# Admin qo'shish
@bot.message_handler(func=lambda message: message.text == "Admin qo'shish ➕")
def add_admin_handler(message):
    msg = bot.reply_to(message, "Adminning ismi va telegram ID sini kiriting (Format: Ismi, TelegramID):")
    bot.register_next_step_handler(msg, process_add_admin)

def process_add_admin(message):
    try:
        full_name, telegram_id = map(str.strip, message.text.split(","))
        create_admin(full_name, telegram_id)
        bot.reply_to(message, f"Admin '{full_name}' muvaffaqiyatli qo'shildi! ✅")
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

# Adminlarni ko'rish
@bot.message_handler(func=lambda message: message.text == "Adminlar 📄")
def list_admins_handler(message):
    admins = get_all_admins()
    if admins:
        response = "Adminlar ro'yxati:\n"
        for admin in admins:
            response += f"ID: {admin[0]}, Ismi: {admin[1]}\n"
    else:
        response = "Hozircha hech qanday admin qo'shilmagan."
    bot.reply_to(message, response)

# Adminni o'chirish
@bot.message_handler(func=lambda message: message.text == "Admini o'chirish 🗑")
def delete_admin_handler(message):
    msg = bot.reply_to(message, "O'chirmoqchi bo'lgan adminning ID raqamini kiriting:")
    bot.register_next_step_handler(msg, process_delete_admin)

def process_delete_admin(message):
    try:
        admin_id = int(message.text.strip())
        result = delete_admin(admin_id)
        bot.reply_to(message, result)
    except ValueError:
        bot.reply_to(message, "ID raqamini to'g'ri formatda kiriting! ❌")
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")


# Inline buttonlar callback datalar uchun
@bot.callback_query_handler(func=lambda call: call.data.startswith("xona_"))
def inline_tugmaga_javob(call):
    """
    Inline tugmalar uchun javob.
    """
    xona_turi_id = int(call.data.split("_")[1])
    natija = bush_xonalar_topish(xona_turi_id)

    if "bush_xonalar" in natija:
        response = f"🏨 *{natija['xona_turi']}* turiga mos bo'sh xonalar:\n\n"
        markup = types.InlineKeyboardMarkup()

        for xona in natija["bush_xonalar"]:
            response += (
                f"🆔 Xona ID: {xona['room_id']}\n"
                f"🛋 Xona turi: {xona['xona_turi']}\n"
                f"📖 Xona haqida: {xona['xona_haqida']}\n\n"
            )
            markup.add(
                types.InlineKeyboardButton(
                    f"Buyurtma qilish - Xona ID {xona['room_id']}",
                    callback_data=f"buyurtma_{xona['room_id']}"
                )
            )

        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode="Markdown")
    else:
        response = natija["message"]
        bot.send_message(call.message.chat.id, response, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buyurtma_"))
def buyurtma_qilish_tugma(call):
    """
    Buyurtma qilish tugmasiga javob.
    """
    xona_id = int(call.data.split("_")[1])

    # Foydalanuvchi ma'lumotlarini yig'ish uchun javobni boshqarish
    user_data[call.message.chat.id] = {'xona_id': xona_id}
    bot.send_message(call.message.chat.id, "Ismingiz va familiyangizni kiriting:")
    bot.register_next_step_handler(call.message, process_full_name)

def process_full_name(message):
    """
    Foydalanuvchi to'liq ismini olish.
    """
    user_data[message.chat.id]['full_name'] = message.text
    bot.send_message(message.chat.id, "Tug'ilgan yilingizni kiriting (masalan: 1995):")
    bot.register_next_step_handler(message, process_birth_year)

def process_birth_year(message):
    """
    Foydalanuvchi tug'ilgan yilini olish.
    """
    user_data[message.chat.id]['tugilgan_yili'] = message.text
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Erkak", callback_data="jinsi_erkak"),
        types.InlineKeyboardButton("Ayol", callback_data="jinsi_ayol")
    )
    bot.send_message(message.chat.id, "Jinsingizni kiriting (Erkak/Ayol):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("jinsi_"))
def process_gender_choice(call):
    """
    Genderni tanlash tugmasiga javob.
    """
    jinsi = call.data.split("_")[1]  # Genderni tanlash uchun callback_data dan ajratish
    user_data[call.message.chat.id]['jinsi'] = jinsi

    # Ask for passport details next
    bot.send_message(call.message.chat.id, "Pasport seriya va raqamini kiriting (masalan: AA1234567):")
    bot.register_next_step_handler(call.message, process_passport)

def process_passport(message):
    """
    Foydalanuvchi pasport ma'lumotlarini olish.
    """
    user_data[message.chat.id]['passport_seriya'] = message.text
    bot.send_message(message.chat.id, "Pasport berilgan yilni kiriting (masalan: 2020):")
    bot.register_next_step_handler(message, process_passport_year)

def process_passport_year(message):
    """
    Foydalanuvchi pasport berilgan yilini olish.
    """
    user_data[message.chat.id]['passport_yili'] = message.text
    bot.send_message(message.chat.id, "Telefon raqamingizni kiriting (+998901234567):")
    bot.register_next_step_handler(message, finalize_order)

def finalize_order(message):
    """
    Buyurtma yakunlash.
    """
    user_data[message.chat.id]['phone_number'] = message.text

    # Collecting data from user_data dictionary
    data = user_data[message.chat.id]
    natija = xona_buyurtma_qilish(
        full_name=data['full_name'],
        tugilgan_yili=data['tugilgan_yili'],
        jinsi=data['jinsi'],
        passport_seriya=data['passport_seriya'],
        passport_yili=data['passport_yili'],
        phone_number=data['phone_number'],
        xona_id=data['xona_id']
    )

    if natija.get("message"):
        bot.send_message(message.chat.id, "✅ Xona muvaffaqiyatli buyurtma qilindi!")
    else:
        bot.send_message(message.chat.id, f"❌ Xatolik qayta urinib ko'ring!")

def process_passport_input(message):
    passport_seriya = message.text.strip()  # Get passport serial number
    order = get_order_by_passport(passport_seriya)  # Call the function to get the order
    if isinstance(order, dict):  # If a single order is found
        response += f"""
ID: {order['ID']}
Ism-familiya: {order['Ism-familiya']}
Tug'ilgan yili: {order["Tug'ilgan yili"]}
Jinsi: {order['Jinsi']}
Passport seriyasi: {order['Passport seriyasi']}
Xona turi: {order['Xona turi']}
Yaratilgan vaqti: {order['Yaratilgan vaqti']}

"""

        bot.send_message(message.chat.id, response)
    else:  # If no order found
        bot.send_message(message.chat.id, order)  # Error message from `get_order_by_passport`

def process_xona_turi_input(message):
    xona_turi = message.text.strip()  # Get the new room type name
    result = xona_turi_qushish(xona_turi)  # Call the function to add the room type
    bot.send_message(message.chat.id, result)  # Send confirmation message to the admin


# Xona qo'shish
def process_room_id_input(message):
    room_id = message.text.strip()  # Get room ID
    bot.send_message(message.chat.id, "Xona turi ID sini kiriting:")
    bot.register_next_step_handler(message, process_xona_turi_id_input, room_id)

def process_xona_turi_id_input(message, room_id):
    xona_turi_id = message.text.strip()  # Get room type ID
    bot.send_message(message.chat.id, "Xona haqida qisqacha ma'lumot kiriting:")
    bot.register_next_step_handler(message, process_xona_haqida_input, room_id, xona_turi_id)

def process_xona_haqida_input(message, room_id, xona_turi_id):
    xona_haqida = message.text.strip()  # Get room description
    bot.send_message(message.chat.id, "Xona band holatida bo'lsinmi? (ha/yoki):")
    bot.register_next_step_handler(message, process_band_xona_input, room_id, xona_turi_id, xona_haqida)

def process_band_xona_input(message, room_id, xona_turi_id, xona_haqida):
    band_xona = True if message.text.strip().lower() == "ha" else False  # Check if the room is occupied
    result = xonalar_qushish(room_id, xona_turi_id, xona_haqida, band_xona)  # Call the function to add the room
    bot.send_message(message.chat.id, result)  # Send confirmation message to the admin

# Botni ishga tushurish
bot.polling(non_stop=True)
