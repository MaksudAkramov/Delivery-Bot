from telebot import types
from django.utils.translation import gettext_lazy as _
import telebot

from apps.bot import bot
from apps.bot import keyboards
from apps.bot.models import BotUser

def request_language(message):
    keyboard = keyboards.get_choose_language_keyboard()
    text = _('Choose language')
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def request_full_name(message):
    keyboard = keyboards.remove_keyboard()
    text = _('Enter your full name')
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def send_hello(message):
    user = BotUser.objects.filter(id=message.from_user.id).first()
    text = _('Hi! Nice to meet you again!')
    keyboard = keyboards.user_keyboard()
    bot.send_message(message.from_user.id, text=str(text),reply_markup=keyboard)


def request_number(message):
    keyboard = keyboards.share_contact_number()
    text = _('Please enter your phone number: ')
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def congrat(message):
    user = BotUser.objects.filter(id=message.from_user.id).first()
    text1 = _("Successful registration")
    text = f"{text1}, {user.full_name}!"
    if user.is_admin:
        keyboard = keyboards.admin_keyboard()
    else:
        keyboard = keyboards.user_keyboard()
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def get_catalog(message: types.Message):    
    text = str(_("Where do we start?"))
    keyboard = keyboards.get_category_keyboard()
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def settings(message:types.Message):
    text = _("What do you want to change?")
    keyboard = keyboards.settings_keyboard()
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def change_name(message: types.Message):
    text = _("Enter your name:")
    keyboard = keyboards.back()
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def send_updated_status(message: types.Message):
    text = _('Updated! Now, you can continue your order')
    keyboard = keyboards.settings_keyboard()
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def back (message: types.Message):
    text = str(_("Return to Homepage"))
    keyboard = keyboards.user_keyboard()
    bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard)


def change_number(message):
    keyboard = keyboards.change_contact_number()
    text = _('Enter your new number')
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)