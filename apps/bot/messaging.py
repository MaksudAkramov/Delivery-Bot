from telebot import types
from django.utils.translation import gettext_lazy as _

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


def back(message: types.Message):
    text = str(_("Return to Homepage"))
    keyboard = keyboards.user_keyboard()
    bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=keyboard)


def change_number(message):
    keyboard = keyboards.change_contact_number()
    text = _('Enter your new number')
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)

def show_product(message, product):
    keyboard = keyboards.add_to_basket_with_back_keyboard()
    name = product.name
    price = product.price
    temp = _("Price:")
    usz = _("Sum")
    text = f"{name} \n\n{temp} {price} {usz}"
    bot.send_photo(message.from_user.id, product.img,str(text),reply_markup=keyboard)


def get_menu(message: types.Message):    
    
    text = str(_("What do you want to order"))
    keyboard = keyboards.get_menu_keyboard()
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def get_category_menu(message: types.Message, cat):    
    text = str(_("Chooce product you want"))
    keyboard = keyboards.get_product_menu_keyboard(cat)
    bot.send_photo(message.from_user.id, photo=open(f"{cat.img}", 'rb'), caption=str(text), reply_markup=keyboard)    

def add_to_basket_message(message: types.Message):
    text = str(_("Add product to cart 🛒")) 
    keyboard = keyboards.add_to_basket_keyboard()
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def choose_quantity_message(message: types.Message):
    text = str(_(f"How many items do you want to purchase? \nIf you want to purchase more than 6 items, write down your number in digits , e.g: 10"))
    keyboard = keyboards.choose_quantity_keyboard()    
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def added_item_message(message, product, quantity):
    keyboard = keyboards.cart_status()
    name = product.name
    quantity = quantity
    quantity_txt = str(_('pc(s) of'))
    status_txt = str(_('added to your cart!'))
    text = f"{quantity} {quantity_txt} {name} {status_txt}"
    bot.send_message(message.from_user.id, str(text), reply_markup=keyboard)  

def anything_else_message(message: types.Message):
    keyboard = keyboards.cart_status()
    text = str(_("Anything else? 😉"))
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def show_cart_items_in_the_beginning_messaging(message, cart_items):
    keyboard = keyboards.cart_items_in_the_beginning_keyboard(cart_items)
    item_list = []
    for item in cart_items:
        item_txt = str({item.product} - {item.quantity})
        item_list.append(item_txt)
    item_list_newline = "\n".join(item_list)
    your_cart_txt = str(_('Your Cart:'))
    text = f"{your_cart_txt} \n{item_list_newline}"
    bot.send_message(message.from_user.id, str(text), reply_markup=keyboard)  

def show_cart_items_messaging(message, cart_items):
    keyboard = keyboards.cart_items_keyboard(cart_items)
    item_list = []
    for item in cart_items:
        item_txt = str({item.product} - {item.quantity})
        item_list.append(item_txt)
    item_list_newline = "\n".join(item_list)
    your_cart_txt = str(_('Your Cart:'))
    text = f"{your_cart_txt} \n{item_list_newline}"
    bot.send_message(message.from_user.id, str(text), reply_markup=keyboard)

def show_empty_cart_items_messaging(message, cart_items):
    keyboard = None
    text = str(_(f"It seems like you didn't put anything into your cart. 😔 \nLet's order something! 😊")) 
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)    

def let_us_continue(message):
    keyboard = keyboards.cart_status()
    text = str(_("Ok, let's continue!"))
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)

def empty_cart_message(message):
    keyboard = None
    text = str(_(f"Your cart is empty, now! \nLet's order something! 😊")) 
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)  

def let_us_fill_the_cart(message):
    keyboard = None
    text = str(_(f"It seems like you didn't put anything into your cart. 😔 \nLet's order something! 😊")) 
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def choose_or_send_new_location_message(message):
    keyboard = keyboards.choose_location_keyboard(message)
    text = str(_("Please choose your last locations or send a new location 📍"))
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)


def deliver_location_message(message, address):
    keyboard = keyboards.confrim_keyboard()
    text1 = str(_('We will deliver to this location:'))
    text2 = str(address)
    user = BotUser.objects.filter(id=message.from_user.id).first()
    user_name = user.full_name
    text = str(_(f"{text1} \n{text2}"))
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)

def let_us_start_from_the_beginning_message(message):
    keyboard = None
    text = str(_("Let's start from the beginning!"))
    bot.send_message(message.from_user.id, text=str(text), reply_markup=keyboard)    








