from telebot import types

from django.utils.translation import gettext_lazy as _

from apps.bot.models import Address, AddressItem, BotUser
from apps.product.models import Category, Product
from apps.product.views import all_categories

def get_category_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    categories = all_categories()
    button1 = types.KeyboardButton(text = str(_("↩️Back")))
    for cat in categories:
        keyboard.add(types.KeyboardButton(text=str(cat)))
    keyboard.add(button1)
    return keyboard

def get_choose_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for lang in BotUser.Locale.choices:
        keyboard.add(types.KeyboardButton(text=str(lang[1])))
    return keyboard

def share_contact_number():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    text=_("Share your phone number📱")
    reg_button = types.KeyboardButton(text=str(text), request_contact=True)
    keyboard.add(reg_button)
    return keyboard

def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    text=_("Add ad")
    button1 = types.KeyboardButton(text=str(text))
    button2 = types.KeyboardButton(text = str(_("⚙️Settings")))
    keyboard.add(button1,button2)

    return keyboard

def user_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text = str(_("⚙️Settings")))
    button2 = types.KeyboardButton(text = str(_("📒Catalog")))
    button3 = types.KeyboardButton(text = str(_("🛒Cart")))
    keyboard.add(button1, button2, button3)

    return keyboard

def settings_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text= str(_("Change language 🌎")))
    button2 = types.KeyboardButton(text= str(_("Change Name")))
    button3 = types.KeyboardButton(text= str(_("Change Phone Number 📱")))
    button4 = types.KeyboardButton(text= str(_("↩️Back")))
    keyboard.add(button1,button2,button3, button4)

    return keyboard

def back():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text= str(_("↩️Back")))
    keyboard.add(button)

    return keyboard


def change_contact_number():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    text=_("Share your phone number📱")
    reg_button = types.KeyboardButton(text=str(text), request_contact=True)
    text=_("Back")
    button = types.KeyboardButton(text=str(text))
    keyboard.add(reg_button, button)
    
    return keyboard
def remove_keyboard():
    return types.ReplyKeyboardRemove()

def get_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text=str(_('↩️Back')))
    buttons = []
    count = 0
    for cat in Category.objects.all():
        text = _(f"{cat.name}")
        menu_button = types.KeyboardButton(text=str(text))
        if count < 2:
            buttons.append(menu_button)
            count += 1
        else:
            count = 0
            keyboard.row(*buttons)
            buttons.clear()
            buttons.append(menu_button)
    keyboard.row(*buttons)
    keyboard.add(button)
    return keyboard


def get_product_menu_keyboard(cat):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text=str(_('↩️Back')))
    buttons = []
    count = 0
    for cat in Product.objects.filter(category = cat).all():
        text = _(f"{cat.name}")
        menu_button = types.KeyboardButton(text=str(text))
        if count < 2:
            buttons.append(menu_button)
            count += 1
        else:
            count = 0
            keyboard.row(*buttons)
            buttons.clear()
            buttons.append(menu_button)
    keyboard.row(*buttons)
    keyboard.add(button)
    return keyboard   

def add_to_basket_with_back_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text=str(_('↩️Back')))
    button2 = types.KeyboardButton(text=str(_('Add product to cart 🛒')))
    keyboard.add(button2, button1)
    return keyboard    


def choose_quantity_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = []
    button1 = types.KeyboardButton(text=str(1))
    button2 = types.KeyboardButton(text=str(2))
    button3 = types.KeyboardButton(text=str(3))
    button4 = types.KeyboardButton(text=str(4))
    button5 = types.KeyboardButton(text=str(5))
    button6 = types.KeyboardButton(text=str(6))
    button7 = types.KeyboardButton(text=str(_('↩️Back')))
    buttons.append(button1)
    buttons.append(button2)
    buttons.append(button3)
    buttons.append(button4)
    buttons.append(button5)
    buttons.append(button6)
    keyboard.row(*buttons)
    keyboard.add(button7)
    return keyboard


def cart_status():    
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text=str(_('🛒Cart')))
    button3 = types.KeyboardButton(text=str(_('Order✅')))
    button2 = types.KeyboardButton(text=str(_('↩️Back')))
    button4 = types.KeyboardButton(text=str(_('Return to catalog 📒')))
    keyboard.add(button2, button1, button3, button4)
    return keyboard

def cart_items_in_the_beginning_keyboard(cart_items):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text=str(_('Empty your cart ♻️')))
    button2 = types.KeyboardButton(text=str(_('Order✅')))
    button = types.KeyboardButton(text=str(_('↩️Back to the beginning')))
    buttons = []
    count = 0
    for item in cart_items:
        text = f"{item.product}"
        menu_button = types.KeyboardButton(text=str(text))
        if count < 2:
            buttons.append(menu_button)
            count += 1
        else:
            count = 0
            keyboard.row(*buttons)
            buttons.clear()
            buttons.append(menu_button)
    keyboard.row(*buttons)
    keyboard.add(button1, button2, button)
    return keyboard  


def cart_items_keyboard(cart_items):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text=str(_('Empty your cart ♻️')))
    button2 = types.KeyboardButton(text=str(_('Order✅')))
    button = types.KeyboardButton(text=str(_('↩️Back')))
    buttons = []
    count = 0
    for item in cart_items:
        text = f"{item.product}"
        menu_button = types.KeyboardButton(text=str(text))
        if count < 2:
            buttons.append(menu_button)
            count += 1
        else:
            count = 0
            keyboard.row(*buttons)
            buttons.clear()
            buttons.append(menu_button)
    keyboard.row(*buttons)
    keyboard.add(button1, button2, button)
    return keyboard    


def change_or_delete_item_from_cart_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = []
    button1 = types.KeyboardButton(text=1)
    button2 = types.KeyboardButton(text=2)
    button3 = types.KeyboardButton(text=3)
    button4 = types.KeyboardButton(text=4)
    button5 = types.KeyboardButton(text=5)
    button6 = types.KeyboardButton(text=6)
    button7 = types.KeyboardButton(text=7)
    button8 = types.KeyboardButton(text=8)
    button9 = types.KeyboardButton(text=9)
    button10 = types.KeyboardButton(text=str(_("Delete item from cart ❌")))
    button11 = types.KeyboardButton(text=str(_('↩️Back')))
    buttons.append(button1)
    buttons.append(button2)
    buttons.append(button3)
    buttons.append(button4)
    buttons.append(button5)
    buttons.append(button6)
    buttons.append(button7)
    buttons.append(button8)
    buttons.append(button9)
    keyboard.row(*buttons)
    keyboard.add(button10, button11)
    return keyboard


def choose_location_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    user = BotUser.objects.filter(id=message.from_user.id).first()
    address_model = Address.objects.filter(user=user).first()
    all_addresses = AddressItem.objects.filter(base=address_model).all()
    
    for adrs in all_addresses:
        keyboard.add(types.KeyboardButton(text=str(adrs)))

    text=_("Send new location 📍")
    button1 = types.KeyboardButton(text=str(text), request_location=True)
    button2 = types.KeyboardButton(text=str(_('❌Cancel order')))
    keyboard.add(button1, button2)

    return keyboard    

def confrim_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = types.KeyboardButton(text=str(_('Confirm✅')))
    button1 = types.KeyboardButton(text=str(_('❌Cancel order')))
    keyboard.add(button, button1)
    return keyboard

def order_more_or_to_beginning():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text=str(_('Order more➕')))
    button2 = types.KeyboardButton(text=str(_('↩️Back to the beginning')))
    keyboard.add(button1, button2)
    return keyboard    
