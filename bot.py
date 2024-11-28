"""
Mualif: Programmers
sana: 25.11.2024
loyiha haiqda: bu loyiha online xona buyurtma qilish uchun qilingan bot.
Bu bot mehmonhonani tanishtiradi va online xona buyurtma qilish uchun ishlashga yordam beradi.
"""




import telebot
from telebot import types
from crud import (
    xona_turi_qushish,
    xonalar_qushish,
    xona_buyurtma_qilish,
    get_user_orders_for_admin,
    get_order_by_passport,
    bush_xonalar_topish
)



TOKEN = "7675610993:AAH5XYiyPXqhMC5mACpaNKZoL1FRjUjUp8Y"


bot = telebot.TeleBot(TOKEN)

ADMINS = [5420071824]



text = """
Assalomu aleykum Xurmatli mijoz sizni botimizga tashrifingizdan bag'oyatda xursandmiz!😇

"""


# response = "📋 *User Orders*\n\n"
# for order in orders:
#     response += (
#         f"🆔 ID: {order['ID']}\n"
#         f"👤 Ism-familiya: {order['Ism-familiya']}\n"
#         f"📅 Tug'ilgan yili: {order['Tug'ilgan yili']}\n"
#         f"👫 Jinsi: {order['Jinsi']}\n"
#         f"📖 Passport: {order['Passport seriyasi']} ({order['Passport yili']})\n"
#         f"🏠 Xona turi: {order['Xona turi']}\n"
#         f"⏰ Yaratilgan vaqti: {order['Yaratilgan vaqti']}\n"
#         "----------------------------\n"
#     )



# foydalanuvchi buyurtmasi alohida qidirgandagi natija
# response = (
#         f"🆔 ID: {order['ID']}\n"
#         f"👤 Ism-familiya: {order['Ism-familiya']}\n"
#         f"📅 Tug'ilgan yili: {order['Tug'ilgan yili']}\n"
#         f"👫 Jinsi: {order['Jinsi']}\n"
#         f"📖 Passport: {order['Passport seriyasi']} ({order['Passport yili']})\n"
#         f"🏠 Xona turi: {order['Xona turi']}\n"
#         f"⏰ Yaratilgan vaqti: {order['Yaratilgan vaqti']}"
#     )



@bot.message_handler(commands=['start'])
def boshlash(message):
    """
    Bu funksiya botga /start buyrug'ini berganda textni chiqarib beradi va menu bar xosil qiladi!
    Menu barda 2ta tugma bo'ldi:
        1-tugma: Xona buyurtma qilish
        2-tugma: Mexmonhona haqida
    degan tugmalarni chiqarib beradi!
    """
    if message.chat.id in ADMINS:
        # Admin panel uchun tugmalar
        tugma = types.ReplyKeyboardMarkup()
        tugma.add("Barcha Buyurtmalar", "Buyurtmani tekshirish")
        tugma.add("Xona qo'shish", "Bo'sh xonalar")
        tugma.add("buyurtma qo'shish")
        tugma.add("Xona turini qo'shish", "Xonalar turini ko'rish")
        bot.send_message(message.chat.id, "Admin paneliga xush kelibsiz!", reply_markup=tugma)
    else:
        tugma = types.ReplyKeyboardMarkup()
        tugma.add("Xona buyurtma qilish", "Mexmonhona haqida")
        bot.send_message(message.chat.id, text, reply_markup=tugma)


# Tugmalardagi qiymatlarga javob berish yani tugmalarga javob berish
@bot.message_handler(content_types=['text'])
def tugmalarga_javob_berish(message):
    if message.text == "Xona buyurtma qilish":
        # Xona turlari uchun inline tugma yaratish
        xonalar = bush_xonalar_topish()
        
        if not xonalar['bosh_xonalar']:
            bot.send_message(message.chat.id, "Hozircha bo'sh xonalar mavjud emas.")
            return

        # Inline tugmalar yaratish
        markup = types.InlineKeyboardMarkup()
        for xona in xonalar['bosh_xonalar']:
            tugma = types.InlineKeyboardButton(
                text=f"Xona ID: {xona['room_id']} ({xona['xona_turi']})",
                callback_data=f"xona_buyurtma:{xona['room_id']}"
            )
            markup.add(tugma)

        # Foydalanuvchiga inline tugmalarni yuborish
        bot.send_message(
            message.chat.id,
            "Quyidagi bo'sh xonalardan birini tanlang:",
            reply_markup=markup
        )


bot.polling()