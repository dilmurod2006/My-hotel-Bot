from telebot import types

# Admin uchun tugmalar
def admin_keyboard():
    """
    Admin uchun maxsus tugmalarni yaratadi.
    
    Bu funktsiya admin paneli uchun zarur bo'lgan tugmalarni yaratadi.
    Tugmalar orasida buyurtmalarni tekshirish, barcha buyurtmalarni ko'rish,
    xona turini qo'shish va sozlamalar mavjud.
    
    Returns:
        types.ReplyKeyboardMarkup: Admin uchun tugmalarni o'z ichiga olgan 
        ReplyKeyboardMarkup obyekti.
    """
    # Admin uchun tugmalarni yaratish
    tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Tugmalarni qo'shish
    tugma.add("Buyurtmani tekshirish 🔎", "Barcha Buyurtmalar 📄")
    tugma.add("Xona turini qo'shish ➕", "Xona qo'shish ➕")
    tugma.add("Sozlamalar ⚙️")
    
    return tugma

# sozlamalar tugmasi
def settings_keyboard():
    tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tugma.add("Admin qo'shish ➕", "Adminlarni ko'rish 📄")
    tugma.add("Asosiy menyu 🏠", "Adminni o'chirish ❌")
    return tugma


# Foydalanuvchi uchun tugmalar
def user_keyboard(lang_code):
    """
    Foydalanuvchi uchun maxsus tugmalarni yaratadi.
    
    Bu funktsiya foydalanuvchi interfeysi uchun zarur bo'lgan tugmalarni yaratadi.
    Tugmalar orasida xona buyurtma qilish va bot haqida ma'lumot olish mavjud.
    Shuningdek, orqa va bekor qilish tugmalari ham qo'shilgan.
    Foydalanuvchining tilini tekshirib, rus, o'zbek va ingliz tillariga mos tugmalarni ko'rsatadi.

    Args:
        lang_code (str): Foydalanuvchining tanlangan tili kodini qabul qiladi.

    Returns:
        types.ReplyKeyboardMarkup: Foydalanuvchi uchun tugmalarni o'z ichiga olgan 
        ReplyKeyboardMarkup obyekti.
    """
    # Foydalanuvchi uchun tugmalarni yaratish
    tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if lang_code == "uz":
        # O'zbek tili uchun tugmalar
        tugma.add("Xona buyurtma qilish", "Bot haqida")
    elif lang_code == "ru":
        # Rus tili uchun tugmalar
        tugma.add("Заказать комнату", "О боте")
    elif lang_code == "en":
        # Ingliz tili uchun tugmalar
        tugma.add("Order a room", "About the bot")
    
    return tugma



def cancel_keyboard():
    """
    Bekor qilish tugmasini yaratadi.
    
    Bu funktsiya foydalanuvchiga yoki admin paneliga amallarni bekor qilish uchun 
    tugma qo'shadi. Ular bekor qilish uchun tugmani bosib, o'z harakatlarini to'xtatishlari mumkin.
    
    Returns:
        types.ReplyKeyboardMarkup: Bekor qilish tugmasini o'z ichiga olgan 
        ReplyKeyboardMarkup obyekti.
    """
    # Bekor qilish tugmasini yaratish
    tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.KeyboardButton("Bekor qilish ❌")
    tugma.add(cancel_button)
    
    return tugma


def back_keyboard():
    """
    Orqa qaytish tugmasini yaratadi.
    
    Bu funktsiya foydalanuvchiga yoki admin paneliga orqaga qaytish tugmasini yaratish 
    imkonini beradi. Foydalanuvchi yoki admin oldingi menyuga qaytishi uchun ushbu tugmani 
    ishlatishi mumkin.
    
    Returns:
        types.ReplyKeyboardMarkup: Orqa qaytish tugmasini o'z ichiga olgan 
        ReplyKeyboardMarkup obyekti.
    """
    # Orqa qaytish tugmasini yaratish
    tugma = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton("Orqa qaytish 🔙")
    tugma.add(back_button)
    
    return tugma


# Til tanlash tugmalari
def language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("🇺🇿 O‘zbekcha", "🇷🇺 Русский", "🇬🇧 English")
    return keyboard
