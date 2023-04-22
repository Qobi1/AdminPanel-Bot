from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.core.management import BaseCommand
from telegrambot.views import *
from webappbot.settings import TOKEN


class Command(BaseCommand):
    def handle(self, *args, **options):
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT, received_message))
        application.add_handler(MessageHandler(filters.CONTACT | filters.LOCATION, received_contact_location))
        application.run_polling()
