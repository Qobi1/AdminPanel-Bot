from django.db import connection

from .text import buttons, dictionary
from telegram.ext import CallbackContext
from telegram import Update
from app1.models import User, Orders, Category, Product
from webappbot.settings import DELIVERY_PRICE, USER_ID


# def dictfetchone(cursor):
#     row = cursor.fetchone()
#     if row is None:
#         return False
#     columns = [col[0] for col in cursor.description]
#     return dict(zip(columns, row))


# Function for start command
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    # print(User.objects.filter(user_id=user.id).query)
    client = User.objects.filter(user_id=user.id).first()
    # with connection.cursor() as cursor:
    #     cursor.execute('Select * from app1_user where user_id=%s', [user.id])
    #     client = dictfetchone(cursor)
    # print(client)

    # checks whether user is in Database
    # data will be created, if user doesn't exist
    if client is None:
        if user.username:
            User.objects.create(user_id=user.id, state=1, username=user.username, log={'order': 0})
        else:
            User.objects.create(user_id=user.id, state=1, log={'order': 0})
        await update.message.reply_text("Tilni tanlang!\nВыберите язык!", reply_markup=buttons(type='lang'))
        return 0
    try:
        User.objects.filter(user_id=user.id).update(state=2)
        await update.message.reply_text(dictionary(client.language, 'greeting') + user.first_name, reply_markup=buttons(type='mainmenu', lang=client.language))
    except:
        await update.message.reply_text("Tilni tanlang!\nВыберите язык!", reply_markup=buttons(type='lang'))


# Function receives all messages from user
async def received_message(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.message.text
    client = User.objects.filter(user_id=user.id).first()
    if client is None:
        if user.username:
            User.objects.create(user_id=user.id, state=1, username=user.username, log={'order': 0})
        else:
            User.objects.create(user_id=user.id, state=1, log={'order': 0})
        await update.message.reply_text("Tilni tanlang!\nВыберите язык!", reply_markup=buttons(type='lang'))
        return 0

    # Adding products for the sake of creating buttons to delete
    products = []
    if client.state == 1:
        if msg in ['🇺🇿O\'zbek', '🇷🇺Русский']:
            await update.message.reply_text(dictionary(msg, 'greeting') + user.first_name, reply_markup=buttons(type='mainmenu', lang=msg))
            User.objects.filter(user_id=user.id).update(state=2, language=msg)
            return 0
        else:
            await update.message.reply_text('❌Xatolik. Berilganlardan birini tanlang!👇', reply_markup=buttons(type='lang'))
            return 0
    client = User.objects.filter(user_id=user.id).first()

    if msg == dictionary(client.language, 'options')[0]:
        result = message(client, products)
        if result == "":
            await update.message.reply_text(dictionary(client.language, 'empty_bin'), reply_markup=buttons(type='ctg', lang=client.language))
            return 0
        await update.message.reply_text(dictionary(client.language, 'delete'))
        await update.message.reply_text(result, parse_mode='HTML', reply_markup=buttons(type='delete', msg=products, lang=client.language))
        return 0
    elif msg == dictionary(client.language, 'options')[1]:
        result = message(client, products)
        if result == "":
            await update.message.reply_text(dictionary(client.language, 'empty_bin'),
                                            reply_markup=buttons(type='ctg', lang=client.language))
            return 0
        elif client.phone_number is None:
            await update.message.reply_text(dictionary(client.language, 'contact'), reply_markup=buttons(type='contact'))
            User.objects.filter(user_id=user.id).update(state=6)
            return 0
        else:
            await update.message.reply_text(dictionary(client.language, 'location'), reply_markup=buttons(type='location'))
            User.objects.filter(user_id=user.id).update(state=7)
            return 0
    elif msg == dictionary(client.language, 'options')[2] and client.state >= 3:
        client.state -= 1
        client.save()
    elif msg == dictionary(client.language, 'options')[3]:
        await update.message.reply_text(dictionary(client.language, 'ctg'), reply_markup=buttons(type='mainmenu', lang=client.language))
        User.objects.filter(user_id=user.id).update(state=2)
        return 0
    elif msg == dictionary(client.language, 'bin')[1]:
        client.log.clear()
        client.log = {'order': '', 'ctg': ''}
        client.save()
        await update.message.reply_text(dictionary(client.language, 'ctg'), reply_markup=buttons(type='ctg', lang=client.language))
        return 0

    elif msg.startswith("❌") and msg.split(" ", 1)[1] in client.log.keys():
        del client.log[msg.split(" ", 1)[1]]
        client.save()
        result = message(client, products)
        if result == "":
            await update.message.reply_text(dictionary(client.language, 'empty_bin'), reply_markup=buttons(type='ctg', lang=client.language))
            return 0
        await update.message.reply_text(dictionary(client.language, 'delete'))
        await update.message.reply_text(result, parse_mode='HTML', reply_markup=buttons(type='delete', msg=products, lang=client.language))
        return 0

    # States
    if client.state == 2:
        MAINMENU = dictionary(client.language, 'mainmenu')
        if msg == MAINMENU[0]:
            User.objects.filter(user_id=user.id).update(state=3)
            await update.message.reply_text(dictionary(client.language, 'ctg'), reply_markup=buttons(type='ctg', lang=client.language))
        elif msg == MAINMENU[1]:
            result = ''
            orders = Orders.objects.filter(user_id=user.id).all()
            if orders:
                for order in orders:
                    result = f"{order.product}"
                    await update.message.reply_text(result, reply_markup=buttons(type='mainmenu', lang=client.language), parse_mode='HTML')
            else:
                await update.message.reply_text(dictionary(client.language, 'empty'), reply_markup=buttons(type='mainmenu', lang=client.language))
        elif msg == MAINMENU[2]:
            User.objects.filter(user_id=user.id).update(state=1)
            await update.message.reply_text("Tilni tanlang!\nВыберите язык!", reply_markup=buttons(type='lang'))
        elif msg == MAINMENU[3]:
            await update.message.reply_text('Empty for now')
        elif msg == MAINMENU[4]:
            client.log['message'] = msg
            client.state = 3
            client.save()
            await update.message.reply_text(dictionary(client.language, 'opinion'), reply_markup=buttons(type='back', lang=client.language))
        else:
            await update.message.reply_text(dictionary(client.language, 'choose_one'), reply_markup=buttons(type='mainmenu', lang=client.language))

    elif client.state == 3:
        if Category.objects.filter(name=msg):
            client.log['ctg'] = msg
            client.state = 4
            client.save()
            await update.message.reply_text(dictionary(client.language, 'ctg'), reply_markup=buttons(type='subctg', lang=client.language, msg=msg))
        elif 'message' in client.log:
            try:
                client.log.pop('message')
                client.state = 2
                client.save()
            except:
                pass
            await context.bot.send_message(USER_ID, msg)
            await update.message.reply_text(dictionary(client.language, 'thanks'), reply_markup=buttons(type='mainmenu', lang=client.language))
        else:
            await update.message.reply_text(dictionary(client.language, 'choose_one'), reply_markup=buttons(type='ctg', lang=client.language))

    elif client.state == 4:
        if Product.objects.filter(name=msg):
            User.objects.filter(user_id=user.id).update(state=5)
            client = User.objects.filter(user_id=user.id).first()
            client.log['order'] = msg
            client.save()
            product = Product.objects.filter(name=msg).values()[0]
            caption = f"{dictionary(client.language, 'reply')[0]}: {product['name']}\n\n{dictionary(client.language, 'reply')[1]}: {product['description']}\n\n{dictionary(client.language, 'reply')[2]}: {product['price']} so'm"
            await context.bot.send_photo(user.id, photo=open(f"media/{product['image']}", 'rb'), caption=caption, reply_markup=buttons(type='numbers', lang=client.language), parse_mode='HTML')
        else:
            await update.message.reply_text(dictionary(client.language, 'choose_one'), reply_markup=buttons(type='subctg', lang=client.language, msg=client.log['ctg']))

    elif client.state == 5:
        if msg.isdecimal():
            value = client.log[f'order']
            client.state = 3
            client.log[value] = int(msg)
            client.save()
            await update.message.reply_text(dictionary(client.language, 'extra'), reply_markup=buttons(type='ctg', lang=client.language))
        else:
            await update.message.reply_text(dictionary(client.language, 'choose_one'), reply_markup=buttons(type='numbers', lang=client.language))

    elif client.state == 6:
        await update.message.reply_text(dictionary(client.language, 'contact'), reply_markup=buttons(type='contact', lang=client.language))
    elif client.state == 7:
        await update.message.reply_text(dictionary(client.language, 'location'), reply_markup=buttons(type='location', lang=client.language))


# Function to handle/receive contact
async def received_contact_location(update: Update, context: CallbackContext):
    user = update.effective_user
    client = User.objects.filter(user_id=user.id).first()
    if client.state == 6:
        contact = update.message.contact.phone_number
        User.objects.filter(user_id=user.id).update(state=7, phone_number=contact)
        await update.message.reply_text(dictionary(client.language, 'location'), reply_markup=buttons(type='location'))
    elif client.state == 7:
        location = update.message.location
        await update.message.reply_text(dictionary(client.language, 'final_step'), reply_markup=buttons(type='mainmenu', lang=client.language))
        await context.bot.sendLocation(chat_id=USER_ID, longitude=location.longitude, latitude=location.latitude)
        result = message(client, phone=client.phone_number)
        order_number = Orders.objects.create(user_id=user.id, phone_number=client.phone_number, product=result[1])
        await context.bot.send_message(chat_id=user.id, text=f"<strong>#Buyurtma raqami</strong>: {order_number.id}\n\n{result[0]}", parse_mode='HTML')
        User.objects.filter(user_id=user.id).update(state=2, log={'order': 0, 'ctg': ''})


def message(client, products=None, phone=None):
    if phone:
        result, prices, result2 = '', 0, ''
        for i in client.log:
            if i in ['order', 'message', 'ctg']:
                continue
            else:
                s = Product.objects.filter(name=i).values()[0]
                prices += s['price'] * client.log[i]
                result += f"{i}\n{client.log[i]} x {s['price']}= {s['price'] * client.log[i]} so'm\n\n"
                result2 += f"{i} ({client.log[i]} x {s['price']}= {s['price'] * client.log[i]} so'm), \n\n"
        function = dictionary(client.language, 'price')
        result += f"{function[0]}: {DELIVERY_PRICE} so'm\n\n\n{function[1]}: {prices + DELIVERY_PRICE} so'm\nRaqami: {phone}"
        result2 += f"{function[0]}: {DELIVERY_PRICE} so'm\n\n\n{function[1]}: {prices + DELIVERY_PRICE} so'm\n\n"
        return result, result2
    else:
        result, prices = '', 0
        for i in client.log:
            if i in ['order', 'message', 'ctg']:
                continue
            else:
                s = Product.objects.filter(name=i).values()[0]
                products.append(i)
                prices += s['price'] * client.log[i]
                result += f"<strong>{i}</strong>\n{client.log[i]} x {s['price']}= {s['price'] * client.log[i]} so'm\n\n"
        if result == "":
            return result
        function = dictionary(client.language, 'price')
        result += f"{function[0]}: {DELIVERY_PRICE} so'm\n\n\n{function[1]}: {prices + DELIVERY_PRICE} so'm\n\n"
        return result