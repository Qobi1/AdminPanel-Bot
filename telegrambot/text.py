from telegram import KeyboardButton, ReplyKeyboardMarkup
from app1.models import Category, Product


def dictionary(language, command):
    dict = {
        "🇺🇿O'zbek": {
            'mainmenu': ['🛍Buyurtma berish', '📦Mening buyurtmalarim', '⚙Sozlamalar', 'ℹBiz haqimizda', '✍Izoh yozib qoldirish'],
            'greeting': f'Salom ',
            'ctg': "Kategoriyalardan birini tanlang",
            'opinion': "O'z fikringizni yozib qoldiring!",
            'choose_one': "❌Xatolik. Berilganlardan birini tanlang!👇",
            'options': ['📥Savatcha', '🛒Buyurtmani yuborish', '⬅Orqaga', '🏠Bosh Menu'],
            'reply': ['Nomi', 'Malumot', 'Narxi']
        },
        '🇷🇺Русский': {

        }
    }

    return dict[language][command]


def buttons(type, lang=None, msg=None):
    btn = []
    if type == 'lang':
        btn = [[KeyboardButton('🇺🇿O\'zbek'), KeyboardButton('🇷🇺Русский')]]
    elif type == 'contact':
        btn = [[KeyboardButton("📞Contact", request_contact=True)]]
    elif type == 'mainmenu':
        MAIN_MENU = dictionary(lang, 'mainmenu')
        btn = [
            [KeyboardButton(MAIN_MENU[0])],
            [KeyboardButton(MAIN_MENU[1]), KeyboardButton(MAIN_MENU[2])],
            [KeyboardButton(MAIN_MENU[3]), KeyboardButton(MAIN_MENU[4])],
        ]
    elif type == 'ctg':
        ctg = Category.objects.all().values()
        for i in range(0, len(ctg) - 1, 2):
            btn.append(
                [KeyboardButton(ctg[i]['name']), KeyboardButton(ctg[i + 1]['name'])]
            )
        if len(ctg) % 2 != 0:
            btn.append([KeyboardButton(ctg[-1]['name'])])
        options = dictionary(lang, 'options')
        for i in range(0, len(options), 2):
            btn.append(
                [KeyboardButton(options[i]), KeyboardButton(options[i + 1])],
            )
    elif type == 'subctg':
        subctg = Product.objects.filter(ctg__name=msg).values()
        for i in range(0, len(subctg) - 1, 2):
            btn.append(
                [KeyboardButton(subctg[i]['name']), KeyboardButton(subctg[i + 1]['name'])]
            )
        if len(subctg) % 2 != 0:
            btn.append([KeyboardButton(subctg.last()['name'])])
        options = dictionary(lang, 'options')
        for i in range(0, len(options), 2):
            btn.append(
                [KeyboardButton(options[i]), KeyboardButton(options[i + 1])],
            )
    elif type == 'numbers':
        for i in range(1, 10, 3):
            btn.append([KeyboardButton(f'{i}'), KeyboardButton(f'{i + 1}'), KeyboardButton(f"{i + 2}")])
        btn.append([KeyboardButton(dictionary(lang, 'options')[0]), KeyboardButton(dictionary(lang, 'options')[2])])
    elif type == 'back':
        btn = [[KeyboardButton(dictionary(lang, 'all')[2])]]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)