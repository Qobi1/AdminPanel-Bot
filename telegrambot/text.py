from telegram import KeyboardButton, ReplyKeyboardMarkup
from app1.models import Category, Product


def dictionary(language, command):
    dict = {
        "🇺🇿O'zbek": {
            'mainmenu': ['🛍Buyurtma berish', '📦Mening buyurtmalarim', '⚙Sozlamalar', 'ℹBiz haqimizda', '✍Izoh yozib qoldirish'],
            'greeting': 'Salom ',
            'ctg': "Kategoriyalardan birini tanlang",
            'opinion': "O'z fikringizni yozib qoldiring!",
            'choose_one': "Berilganlardan birini tanlang!👇",
            'options': ['📥Savatcha', '🛒Buyurtmani yuborish', '⬅Orqaga', '🏠Bosh Menu'],
            'reply': ['<strong>Nomi</strong>', '<strong>Malumot</strong>', '<strong>Narxi</strong>'],
            'bin': ['⬅Orqaga', "🔄O'chirish", "🛒Buyurtmani yuborish"],
            'thanks': "Bildirgan fikringiz uchun minnatdormiz",
            'empty': 'Sizda hechqanday buyurtmalar yo\'q',
            'contact': "Telefon raqamingizni yuboring👇",
            'extra': "Mahsulot savatchaga qo'shildi. Yana biror nma hohlaysizmi",
            'delete': "❌ Mahsulot nomi - savatdan olib tashlash\n🔄 O'chirish - savatni bo'shatish",
            'price': ['Dastavka', 'Umumiy'],
            'empty_bin': "Sizning savatingizda hechnima yo'q",
            'location': "Manzilingizni kriting!👇",
            'final_step': "Xaridingiz uchun minatdorchilik bildiramz. Biz siz blan bog'lanamiz"
        },
        '🇷🇺Русский': {
            'mainmenu': ['🛍 Заказать', '📦 Мои заказы', '⚙Настройки', 'ℹО нас', '✍Обратная связь'],
            'greeting': 'Привет ',
            'ctg': 'Выберите одну из категорий',
            'opinion': 'Напишите свое мнение!',
            'choose_one': 'Не найдено товара с таким названием',
            'options': ['📥 Корзина', '🛒Отправка заказа', '⬅Назад', '🏠Главное меню'],
            'reply': ['<strong>Имя</strong>', '<strong>Информация</strong>', '<strong>Цена</strong>'],
            "bin": ['⬅Назад', "🔄 Очистить", '🛒Отправка заказа'],
            'thanks': 'Спасибо за ваш отзыв',
            'empty': 'У вас нет заказов',
            'contact': "Отправьте свой номер телефона👇",
            'extra': 'Товар добавлен в корзину, что нибудь еще?',
            'delete': """❌ Название продукта» - удалить из корзины\n🔄 Очистить» - полностью очистить корзину""",
            'price': ['Доставка', 'Итого'],
            'empty_bin': 'У вас ничего нет в корзине',
            'location': 'Введите свой адрес!👇',
            'final_step': 'Спасибо за покупку. Мы вам позвоним'
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
            btn.append([KeyboardButton(ctg.last()['name'])])
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
        btn = [[KeyboardButton(dictionary(lang, 'options')[2])]]
    elif type == 'delete':
        for i in msg:
            btn.append([KeyboardButton(f"❌ {i}")])
        function = dictionary(lang, 'bin')
        btn.append([KeyboardButton(function[0]), KeyboardButton(function[1])])
        btn.append([KeyboardButton(function[2])])
    elif type == "location":
        btn.append([KeyboardButton('📍Lokatsiya', request_location=True)])
    return ReplyKeyboardMarkup(btn, resize_keyboard=True)