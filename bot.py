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
    get_all_room_types,
    get_available_rooms
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
# TOKEN = "8138018168:AAERImAlc1u0h_dWm5UOQbO9OKwlg-7Pvr0"
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
user_data = {}  # Dictionary to maintain user data
@bot.message_handler(func=lambda message: message.text == "Xona buyurtma qilish")
def xona_buyurtma(message):
    markup = types.InlineKeyboardMarkup()
    xona_turi = get_all_room_types()  # Xona turlari ro'yxatini olish
    if xona_turi:
        for xona in xona_turi:
            markup.add(types.InlineKeyboardButton(xona[1], callback_data=f"xona_{xona[0]}"))
        bot.send_message(message.chat.id, "Xona turini tanlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Hozircha hech qanday xona turi mavjud emas.")

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
                f"💰 Narx: {xona['price']} so'm\n\n"
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
    bot.register_next_step_handler(message, get_start_date)

def get_start_date(message):
    """
    Foydalanuvchi telefon raqamini olish.
    """
    user_data[message.chat.id]['phone_number'] = message.text
    bot.send_message(message.chat.id, "Xonadaga borish sanangizni kiriting (masalan: 01.01.2023 14:00):")
    bot.register_next_step_handler(message, get_end_date)

def get_end_date(message):
    """
    Foydalanuvchi xonadagi borish tugash sanasini olish.
    """
    user_data[message.chat.id]['start_date'] = message.text
    bot.send_message(message.chat.id, "Xonadagi tugash sanangizni kiriting (masalan: 01.01.2023 14:00):")
    bot.register_next_step_handler(message, tulov_qilish)

def tulov_qilish(message):
    """
    Buyurtma yakunlash.
    """
    user_data[message.chat.id]['end_date'] = message.text

    # Collecting data from user_data dictionary
    markup = types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()
    markup.add(
    types.InlineKeyboardButton("Click", callback_data="Click"),
    types.InlineKeyboardButton("Payme", callback_data="payme"),
    types.InlineKeyboardButton("Uzcard", callback_data="uzcard"),
    types.InlineKeyboardButton("Humo", callback_data="humo"),
    types.InlineKeyboardButton("Visa", callback_data="visa"),
    types.InlineKeyboardButton("Mastercard", callback_data="mastercard")
)


    bot.send_message(message.chat.id, "Tulov turini tanlang", reply_markup=markup)

# to'lov amalga oshirish
@bot.callback_query_handler(func=lambda call: True)
def tulov_callback_handler(call):
    if call.data in ["Click", "payme", "uzcard", "humo", "visa", "mastercard"]:
        bot.send_message(call.message.chat.id, f"{call.data} raqamini kiriting")
        bot.register_next_step_handler(call.message, get_card_data)

# get card data
def get_card_data(message):
    """"Kartani ma'lumotlarini olish"""
    bot.send_message(message.chat.id, "oldindan 30% to'lov amalga oshirildi ✅")
    bot.register_next_step_handler(message, finalize_order)


def finalize_order(message):
    """
    Buyurtma yakunlash.
    """
    user_data[message.chat.id]['end_date'] = message.text

    # Collecting data from user_data dictionary
    data = user_data[message.chat.id]
    natija = xona_buyurtma_berish(
        full_name=data['full_name'],
        tugilgan_yili=data['tugilgan_yili'],
        jinsi=data['jinsi'],
        passport_seriya=data['passport_seriya'],
        passport_yili=data['passport_yili'],
        phone_number=data['phone_number'],
        xona_raqami=data['xona_id'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )

    if natija.get("message"):
        bot.send_message(message.chat.id, "✅ Xona muvaffaqiyatli buyurtma qilindi!")
    else:
        bot.send_message(message.chat.id, f"❌ Xatolik qayta urinib ko'ring!")





# Botdagi ma'lumotlarni vaqtincha saqlash uchun lug'at




# users panel stop




# Botni ishga tushurish
bot.polling(non_stop=True)
