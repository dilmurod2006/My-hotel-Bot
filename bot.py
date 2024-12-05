import telebot
from telebot import types
from deep_translator import GoogleTranslator
import pickle
from crud import (
    xona_turi_qushish,
    xona_qushish,
    xona_buyurtma_berish,
    get_user_orders_for_admin,
    get_order_by_passport,
    bush_xonalar_topish,
    create_admin,
    delete_admin,
    get_all_admins,
    get_all_room_types
)
from tugmalar import (
    user_keyboard,
    admin_keyboard,
    cancel_keyboard,
    back_keyboard,
    language_keyboard,
    settings_keyboard
)

TOKEN = "7675610993:AAEZzNcQJpGWTOctlGx9cjbulGsvTkogv0g"
bot = telebot.TeleBot(TOKEN)

ADMINS = [1231232131, 7054004046, 5420071824]

text = """
Assalomu aleykum Xurmatli mijoz! Sizni botimizga tashrifingizdan bag'oyatda xursandmiz! 😇
"""

# Foydalanuvchi tillarini saqlash uchun fayl
LANGUAGE_FILE = "tillar.pkl"

# Faylni o'qish funksiyasi
def load_languages():
    try:
        with open(LANGUAGE_FILE, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

# Faylga yozish funksiyasi
def save_languages(data):
    with open(LANGUAGE_FILE, "wb") as file:
        pickle.dump(data, file)

# Foydalanuvchi tillarini yuklash
user_languages = load_languages()

# Tilni o'zgartirish funksiyasi
def set_language(user_id, lang_code):
    user_languages[user_id] = lang_code
    save_languages(user_languages)

# Foydalanuvchining tanlangan tilini olish
def get_language(user_id):
    return user_languages.get(user_id, "uz")  # Standart til - o‘zbekcha

# Tarjima funksiyasi
def translate_text(text, lang_code):
    if lang_code == "uz":
        return text  # O‘zbek tilida tarjima kerak emas
    try:
        return GoogleTranslator(source="uz", target=lang_code).translate(text)
    except Exception as e:
        return f"Tarjima xatoligi yuz berdi: {e}"


# Tilni tanlashdan so'ng xabar va rasm yuborish
def send_welcome_with_images(chat_id, lang_code):
    # Yuboriladigan rasm va matn
    welcome_text = translate_text(
        "KalibriHotel Botiga Xush Kelibsiz! 🌟\n\nMehmonxona xonalarini oson va tez bron qilish imkoniyatiga ega bo'ling. "
        "Bizning xizmatimizning afzalliklari:\n\n"
        "- Arzon va qulay narxlar: Yuqori sifat, past narx!\n"
        "- Vaqtni tejash: Hech qanday navbat kutmasdan, istalgan xonani onlayn band qiling.\n"
        "- Oldindan 20% to'lov: Xonani band qilish uchun faqat 20% to'lov qilishingiz kerak, qolganini esa keyinroq to'lashingiz mumkin.\n\n"
        "Sizni KalibriHotel bilan qulay va xavfsiz turizm tajribasi kutmoqda. Hozir bron qilishni boshlang va biz bilan dam olishning yangi darajasiga qadam qo'ying! ✨",
        lang_code
    )
    # Rasm fayllarini yuborish
    image_path = "rasm1.jpg"
    with open(image_path, "rb") as photo:
        bot.send_photo(chat_id, photo, caption=welcome_text,reply_markup=user_keyboard(lang_code))

# Boshlash komandasi
@bot.message_handler(commands=['start'])
def start(message):
    # Admini tekshirish
    if message.chat.id in ADMINS:
        bot.send_message(message.chat.id, "Assalomu aleykum!\nAdmin paneliga xush kelibsiz!", reply_markup=admin_keyboard())
    
    else:
        bot.send_message(
        message.chat.id,
        "Tilni tanlang / Выберите язык / Choose a language",
        reply_markup=language_keyboard()
    )

# Til tanlash
@bot.message_handler(func=lambda msg: msg.text in ["🇺🇿 O‘zbekcha", "🇷🇺 Русский", "🇬🇧 English"])
def select_language(message):
    user_id = message.chat.id
    if message.text == "🇺🇿 O‘zbekcha":
        lang_code = "uz"
    elif message.text == "🇷🇺 Русский":
        lang_code = "ru"
    else:
        lang_code = "en"

    # Tanlangan tilni saqlash
    set_language(user_id, lang_code)
    bot.send_message(
        message.chat.id,
        translate_text("Til tanlandi! Endi xizmatimizdan tanlagan tilda foydalanishingiz mumkin.", lang_code)
    )

    # Rasm va xabar yuborish
    send_welcome_with_images(message.chat.id, lang_code)


# ADMINSTRATOR PANELI START

# sozlamalar menusi
@bot.message_handler(func=lambda msg: msg.text == "Sozlamalar ⚙️")
def show_settings(message):
    if message.chat.id in ADMINS:
        bot.send_message(
            message.chat.id,
            "Sozlamalar menyusiga xush kelibsiz! 🌟\n\n",
            reply_markup=settings_keyboard()
        )
    else:pass
# asosiy menuga qaytish
@bot.message_handler(func=lambda msg: msg.text == "Asosiy menyu 🏠")
def back_to_main_menu(message):
    # Asosiy menuga qaytish
    if message.chat.id in ADMINS:
        bot.send_message(message.chat.id, "Asosiy menuga qaytildi! 🏠", reply_markup=admin_keyboard())
    else:pass

# admin qo'shish start
@bot.message_handler(func=lambda message: message.text == "Admin qo'shish ➕")
def add_admin(message):
    bot.send_message(message.chat.id, "Iltimos, yangi adminning to'liq ismini kiriting:")
    bot.register_next_step_handler(message, get_full_name)

def get_full_name(message):
    full_name = message.text
    bot.send_message(message.chat.id, f"Adminning Telegram ID sini kiriting:")
    bot.register_next_step_handler(message, get_telegram_id, full_name)

def get_telegram_id(message, full_name):
    telegram_id = message.text
    create_admin(full_name, telegram_id)
    bot.send_message(message.chat.id, f"Admin {full_name} muvaffaqiyatli qo'shildi!")
    bot.send_message(message.chat.id, "Sozlamalar uchun 'Sozlamalar' tugmasini bosing.", reply_markup=admin_keyboard())

# admin qo'shish stop

# adminlarni ko'rish
@bot.message_handler(func=lambda message: message.text == "Adminlarni ko'rish 📄")
def show_admins(message):
    admins = get_all_admins()
    if admins:
        admins_list = "\n".join([f"ID: {admin[0]}, Ismi: {admin[1]}" for admin in admins])
        bot.send_message(message.chat.id, f"Hozirgi adminlar:\n{admins_list}")
    else:
        bot.send_message(message.chat.id, "Hech qanday admin topilmadi.")
    bot.send_message(message.chat.id, "Sozlamalar uchun 'Sozlamalar' tugmasini bosing.", reply_markup=admin_keyboard())

# adminlarni ko'rish stop

# adminni o'chirish
@bot.message_handler(func=lambda message: message.text == "Adminni o'chirish ❌")
def delete_admin_prompt(message):
    bot.send_message(message.chat.id, "Iltimos, o'chirishni xohlagan adminning ID sini kiriting:")
    bot.register_next_step_handler(message, delete_admin_by_id)

def delete_admin_by_id(message):
    admin_id = message.text
    result = delete_admin(admin_id)
    bot.send_message(message.chat.id, result)
    bot.send_message(message.chat.id, "Sozlamalar uchun 'Sozlamalar' tugmasini bosing.", reply_markup=admin_keyboard())

# adminni o'chirish stop

# xona turini qo'shish start
@bot.message_handler(func=lambda message: message.text == "Xona turini qo'shish ➕")
def add_xona_turi(message):
    bot.send_message(message.chat.id, "Iltimos, yangi xona turining nomini kiriting:")
    bot.register_next_step_handler(message, get_xona_turi)

def get_xona_turi(message):
    xona_turi = message.text
    result = xona_turi_qushish(xona_turi)
    bot.send_message(message.chat.id, result)
    bot.send_message(message.chat.id, "Sozlamalar uchun 'Sozlamalar' tugmasini bosing.", reply_markup=admin_keyboard())

# xona turini qo'shish stop


# xona qo'shish start
@bot.message_handler(func=lambda message: message.text == "Xona qo'shish ➕")
def add_room(message):
    room_types = get_all_room_types()
    if room_types:
        markup = types.InlineKeyboardMarkup()
        for room in room_types:
            markup.add(types.InlineKeyboardButton(room[1], callback_data=f"room_type_{room[0]}"))
        bot.send_message(message.chat.id, "Xona turini tanlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Hech qanday xona turi mavjud emas.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("room_type_"))
def handle_room_type_selection(call):
    xona_turi_id = int(call.data.split('_')[2])
    bot.send_message(call.message.chat.id, "Xona raqamini kiriting:")
    bot.register_next_step_handler(call.message, get_room_number, xona_turi_id)

def get_room_number(message, xona_turi_id):
    try:
        xona_raqami = int(message.text)
        bot.send_message(message.chat.id, "Xona haqida ma'lumot kiriting:")
        bot.register_next_step_handler(message, get_room_info, xona_turi_id, xona_raqami)
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos, to'g'ri xona raqamini kiriting.")

def get_room_info(message, xona_turi_id, xona_raqami):
    xona_haqida = message.text
    bot.send_message(message.chat.id, "Xonaning narxini kiriting:")
    bot.register_next_step_handler(message, get_room_price, xona_turi_id, xona_raqami, xona_haqida)

def get_room_price(message, xona_turi_id, xona_raqami, xona_haqida):
    try:
        price = int(message.text)
        result = xona_qushish(xona_raqami, xona_turi_id, xona_haqida, price)
        bot.send_message(message.chat.id, result)
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos, to'g'ri narxni kiriting.")

# xona qo'shish stop


# buyurtmani tekshirish start
@bot.message_handler(func=lambda message: message.text == "Buyurtmani tekshirish 🔎")
def check_order(message):
    bot.send_message(message.chat.id, "Iltimos, tekshirish uchun buyurtma ID sini kiriting:")
    bot.register_next_step_handler(message, get_passport_seriya)

def get_passport_seriya(message):
    order_id = message.text
    result = get_order_by_passport(order_id)
    
    # Agar buyurtma topilmasa, xatolik xabari yuborish
    if isinstance(result, str):
        bot.send_message(message.chat.id, result)
    else:
        # Chiroyli formatda ma'lumotni yuborish
        formatted_result = f"""
Buyurtma ma'lumotlari:

🆔: {result['ID']}
Ism-familiya: {result['Ism-familiya']}
Tug'ilgan yili: {result["Tug'ilgan yili"]}
Jinsi: {result['Jinsi']}
Passport seriyasi: {result['Passport seriyasi']}
Passport yili: {result['Passport yili']}
Xona turi: {result['Xona turi']}
Yaratilgan vaqti: {result['Yaratilgan vaqti']}
"""
        bot.send_message(message.chat.id, formatted_result)
    
    # Sozlamalar tugmasini yuborish
    bot.send_message(message.chat.id, "Sozlamalar uchun 'Sozlamalar' tugmasini bosing.", reply_markup=admin_keyboard())

# buyurtmani tekshirish stop


# barcha buyurtmalar start
@bot.message_handler(func=lambda message: message.text == "Barcha Buyurtmalar 📄")
def barcha_buyurtmalar(message):
    orders = get_user_orders_for_admin()
    formatted_orders = ""
    for order in orders:
        formatted_orders += f"""
🆔: {order['ID']}
Ism-familiya: {order['Ism-familiya']}
Tug'ilgan yili: {order["Tug'ilgan yili"]}
Jinsi: {order['Jinsi']}
Passport seriyasi: {order['Passport seriyasi']}
Passport yili: {order['Passport yili']}
Xona turi: {order['Xona turi']}
Yaratilgan vaqti: {order['Yaratilgan vaqti']}
\n
"""
    bot.send_message(message.chat.id, formatted_orders)
    bot.send_message(message.chat.id, "Sozlamalar uchun 'Sozlamalar' tugmasini bosing.", reply_markup=admin_keyboard())

# barcha buyurtmalar stop


# ADMISTRATOR PANELI STOP


# users panel start

# users panel stop




# Botni ishga tushurish
bot.polling(non_stop=True)
