from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.core.management import BaseCommand
from telegrambot.views import *
TOKEN = "5028779716:AAHPX6MXluEDtwPUHfoaG17SbZcqI2rpejw"
USER_ID = 12


class Command(BaseCommand):
    def handle(self, *args, **options):
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT, received_message))
        application.add_handler(MessageHandler(filters.CONTACT, received_contact))
        application.run_polling()
