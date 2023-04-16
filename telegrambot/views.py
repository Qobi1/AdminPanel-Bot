from .text import buttons, dictionary
from telegram.ext import CallbackContext
from telegram import Update, Bot
from app1.models import User, Orders, Category, Product


# Function for start command
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    client = User.objects.filter(user_id=user.id).first()
    # checks whether user is in Database
    if client is None:
        User.objects.create(user_id=user.id, state=1, log={'order': 0})
        await update.message.reply_text("Tilni tanlang!\nВыберите язык!", reply_markup=buttons(type='lang'))
        return 0
    User.objects.filter(user_id=user.id).update(state=2)
    await update.message.reply_text(dictionary(client.language, 'greeting') + user.first_name, reply_markup=buttons(type='mainmenu', lang=client.language))


# Function receives all messages from user
async def received_message(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.message.text
    client = User.objects.filter(user_id=user.id).first()

    if client.state == 1:
        if msg in ['🇺🇿O\'zbek', '🇷🇺Русский']:
            await update.message.reply_text(dictionary(msg, 'greeting') + user.first_name, reply_markup=buttons(type='mainmenu', lang=msg))
            User.objects.filter(user_id=user.id).update(state=2, language=msg)
        else:
            await update.message.reply_text('❌Xatolik. Berilganlardan birini tanlang!👇', reply_markup=buttons(type='lang'))

    elif client.state == 2:
        MAINMENU = dictionary(client.language, 'mainmenu')
        if msg == MAINMENU[0]:
            User.objects.filter(user_id=user.id).update(state=3)
            await update.message.reply_text(dictionary(client.language, 'ctg'), reply_markup=buttons(type='ctg', lang=client.language))
        elif msg == MAINMENU[1]:
            orders = Orders.objects.filter(user_id=user.id).all()
            for order in orders:
                caption = f"User ID:{order.user_id}\n\nTelefon raqami: {order.phone_number}\n\nKategoriya: {order.ctg}\n\nMaxsulot: {order.product}\n\nSoni: {order.numbers}\n\nBuyurtma Voqti: {order.created_at}"
                await context.bot.send_photo(user.id, photo=open(order.image, 'rb'), caption=caption)
        elif msg == MAINMENU[2]:
            User.objects.filter(user_id=user.id).update(state=1)
            await update.message.reply_text("Tilni tanlang!\nВыберите язык!", reply_markup=buttons(type='lang'))
        elif msg == MAINMENU[3]:
            await update.message.reply_text('Empty for now')
        elif msg == MAINMENU[4]:
            User.objects.filter(user_id=user.id).update(state=3)
            await update.message.reply_text(dictionary(client.language, 'opinion'), reply_markup=buttons(type='back'))
        else:
            await update.message.reply_text(dictionary(client.language, 'choose_one'), reply_markup=buttons(type='mainmenu', lang=client.language))

    elif client.state == 3:
        if Category.objects.filter(name=msg):
            User.objects.filter(user_id=user.id).update(state=4)
            await update.message.reply_text(dictionary(client.language, 'ctg'), reply_markup=buttons(type='subctg', lang=client.language, msg=msg))
        else:
            await update.message.reply_text(dictionary(client.language, 'choose_one'), reply_markup=buttons(type='ctg', lang=client.language))

    elif client.state == 4:
        if Product.objects.filter(name=msg):
            User.objects.filter(user_id=user.id).update(state=5)
            client.log[f'{msg}'] = 1
            client.save()
            product = Product.objects.filter(name=msg).values()[0]
            caption = f"{dictionary(client.language, 'reply')[0]}: {product['name']}\n\n{dictionary(client.language, 'reply')[1]}: {product['description']}\n\n{dictionary(client.language, 'reply')[2]}: {product['price']}"
            await context.bot.send_photo(user.id, photo=open(f"media/{product['image']}", 'rb'), caption=caption, reply_markup=buttons(type='numbers', lang=client.language))
        else:
            await update.message.reply_text(dictionary(client.language, 'choose_one'), reply_markup=buttons(type='ctg', lang=client.language))
            User.objects.filter(user_id=user.id).update(state=3)

    elif client.state == 5:
        if int(msg):
            User.objects.filter(user_id=user.id).update(state=3)
            client.log[f'{msg}'] = msg
            await update.message.reply_text(dictionary(client.language, 'ctg'), reply_markup=buttons(type='ctg', lang=client.language))
        else:
            pass


# Function to handle/receive contact
async def received_contact(update: Update, context: CallbackContext):
    contact = update.message.contact
    user = update.effective_user
    client = User.objects.filter(user_id=user.id).first()


async def send_message(request):
    users = User.objects.all().values()
    print(request)
    if request.FILES:
        for user in users:
            await Bot.send_photo(user['user_id'], photo=open(f"media/{request.FILES.get('image')}", 'rb'), caption='123')


