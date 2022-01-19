from telebot import types
from geopy.geocoders import Nominatim

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _

from apps.bot import bot
from apps.bot import messaging
from apps.bot.utils import change_locale, with_locale
from apps.bot.models import Address, AddressItem, BotUser

from apps.cart.models import Cart, CartItem

from apps.product.models import Category, Product


@csrf_exempt
def handle(request):
    request_body_dict = request.body.decode('UTF-8')
    update = types.Update.de_json(request_body_dict)
    bot.process_new_updates([update])
    return HttpResponse(200)


@bot.message_handler(commands=['start'])
@with_locale
def on_start(message: types.Message):
    user_id = message.from_user.id
    if BotUser.objects.filter(id=user_id).exists():
        messaging.send_hello(message)
        bot.register_next_step_handler(message, on_command_specified)
    else:
        messaging.request_language(message)
        bot.register_next_step_handler(message, on_language_specified)

@with_locale
def on_language_specified(message):
    locale = BotUser.Locale.get_from_value(message.text)
    BotUser.objects.update_or_create(id=message.from_user.id, locale=locale)
    with change_locale(locale):
        messaging.request_full_name(message)
        bot.register_next_step_handler(message, on_full_name_specified)

@with_locale
def on_full_name_specified(message):
    
    full_name = str(message.text)
    BotUser.objects.update(id=message.from_user.id, full_name=full_name)
    messaging.request_number(message)
    bot.register_next_step_handler(message, on_number_specified)

@with_locale
def on_number_specified(message):
    if message.contact is not None:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text
    BotUser.objects.update(id=message.from_user.id, phone_number = phone_number)
    messaging.congrat(message)
    bot.register_next_step_handler(message, on_command_specified)

@with_locale
def on_command_specified(message: types.Message):
    user = BotUser.objects.filter(id=message.from_user.id).first()
    cart = Cart.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(cart=cart).all()
    cat = Category.objects.first()
    if message.text == str(_("⚙️Settings")):
        messaging.settings(message)
        bot.register_next_step_handler(message, on_changes_specified)
    if message.text ==str(_("📒Catalog")):
        messaging.get_catalog(message)
        bot.register_next_step_handler(message, on_order_specified)
    else:
        bot.register_next_step_handler(message, on_command_specified)
    if message.text == str(_("🛒Cart")):
        if Cart.objects.filter(user=user).first():
            messaging.show_cart_items_messaging(message, cart_items)
            bot.register_next_step_handler(message, change_or_continue_your_order, cat, cart)
        elif Cart.objects.filter(user=user).first() is None or cart_items is None:
            messaging.show_empty_cart_items_messaging(message, cart_items)
            messaging.get_catalog(message)
            bot.register_next_step_handler(message, on_order_specified)


@with_locale
def on_changes_specified(message: types.Message):
    if message.text == str(_("Change language 🌎")):
        messaging.request_language(message)
        bot.register_next_step_handler(message, on_language_change_specified)
    elif message.text == str(_("Change Name")):
        messaging.change_name(message)
        bot.register_next_step_handler(message, on_name_change_specified)
    elif message.text == str(_("Change Phone Number 📱")):
        messaging.change_number(message)
        bot.register_next_step_handler(message, on_number_change_specified)
    elif message.text == str(_("↩️Back")):
        messaging.back(message)
        bot.register_next_step_handler(message, on_command_specified)

@with_locale
def on_name_change_specified(message: types.Message):
    if message.text == str(_("↩️Back")):
        messaging.back(message)
        bot.register_next_step_handler(message, on_command_specified)
    else:
        full_name = str(message.text)
        BotUser.objects.update(id=message.from_user.id, full_name = full_name)
        messaging.send_updated_status(message)
        bot.register_next_step_handler(message, on_changes_specified)

@with_locale
def on_language_change_specified(message: types.Message):
        locale = BotUser.Locale.get_from_value(message.text)
        BotUser.objects.update(id=message.from_user.id, locale = locale)
        messaging.send_updated_status(message)
        bot.register_next_step_handler(message, on_changes_specified)

@with_locale
def on_number_change_specified(message):
    if message.text == str(_("↩️Back")):
        messaging.back(message)
        bot.register_next_step_handler(message, on_command_specified)
    else:
        if message.contact is not None:
            phone_number = message.contact.phone_number
        else:
            phone_number = message.text
        BotUser.objects.update(id=message.from_user.id, phone_number = phone_number)
        messaging.send_updated_status(message)
        bot.register_next_step_handler(message, on_changes_specified)

@with_locale
def on_order_specified(message: types.Message):
    if message.text == str(_("↩️Back")):
            messaging.back(message)
            bot.register_next_step_handler(message, on_command_specified)
    categories = Category.objects.all()
    for cat in categories:
        if message.text == cat.name:
            messaging.get_category_menu(message,cat)
            bot.register_next_step_handler(message, choose_product, cat)

@with_locale
def choose_product(message,cat):
    product = Product.objects.filter(name = str(message.text)).first()
    if message.text == str(_('↩️Back')):
        messaging.get_catalog(message)
        bot.register_next_step_handler(message, on_order_specified)
    if product is not None:
        messaging.show_product(message,product)
        bot.register_next_step_handler(message, detail_product, cat, product)



@with_locale
def detail_product(message, cat, product):
    if message.text == str(_('↩️Back')):
        messaging.get_category_menu(message, cat)
        bot.register_next_step_handler(message, choose_product, cat)
    if message.text == str(_('Add product to cart 🛒')):
        messaging.choose_quantity_message(message)
        bot.register_next_step_handler(message, add_quantity, product, cat)
        
        


@with_locale        
def add_quantity(message, product, cat):
    user = BotUser.objects.filter(id=message.from_user.id).first()

    if message.text == str(_('↩️Back')):
        messaging.get_category_menu(message, cat)
        bot.register_next_step_handler(message, choose_product, cat)

    if message.text:
        quantity = int(message.text)   


    cart = Cart.objects.filter(user=user).first()
    if not cart:
        cart = Cart.objects.create(user=user)
    CartItem.objects.update_or_create(product=product, quantity=quantity, cart=cart)

    messaging.added_item_message(message, product, quantity) 
    messaging.anything_else_message(message)    
                                   
    bot.register_next_step_handler(message, check_cart, cat, cart)

@with_locale  
def check_cart(message, cat, cart):
    user = BotUser.objects.filter(id=message.from_user.id).first()
    if message.text == str(_('↩️Back')):
        messaging.get_category_menu(message, cat)
        bot.register_next_step_handler(message, choose_product, cat)

    cart_items = CartItem.objects.filter(cart=cart).all()
    if message.text == str(_('🛒Cart')):
        if Cart.objects.filter(user=user).first():
            messaging.show_cart_items_messaging(message, cart_items)
            bot.register_next_step_handler(message, change_or_continue_your_order, cat, cart)
        elif Cart.objects.filter(user=user).first() is None or cart_items is None:
            messaging.show_empty_cart_items_messaging(message, cart_items)
            messaging.get_catalog(message)
            bot.register_next_step_handler(message, on_order_specified)

    if message.text == str(_('Order✅')):
        messaging.choose_or_send_new_location_message(message)
        bot.register_next_step_handler(message, get_address)  

    if message.text ==str(_('Return to catalog 📒')):
        messaging.get_catalog(message)
        bot.register_next_step_handler(message, on_order_specified)

@with_locale  
def change_or_continue_your_order(message, cat, cart):
    if message.text == str(_('↩️Back')):
        messaging.let_us_continue(message)
        bot.register_next_step_handler(message, check_cart, cat, cart)
    if message.text == str(_('↩️Back to the beginning')):
        messaging.back(message)
        bot.register_next_step_handler(message, on_command_specified)
    if message.text == str(_('Empty your cart ♻️')):
        user = BotUser.objects.filter(id=message.from_user.id).first()
        cart = Cart.objects.filter(user=user).first()
        cart_items = CartItem.objects.filter(cart=cart).all()
        if Cart.objects.filter(user=user).first():
            Cart.objects.filter(user=user).delete()
            messaging.empty_cart_message(message)
        elif Cart.objects.filter(user=user).first() is None or cart_items is None:
            messaging.let_us_fill_the_cart(message)
            


        messaging.let_us_continue(message)
        bot.register_next_step_handler(message, check_cart, cat, cart)
    if message.text == str(_('Order✅')):
        messaging.choose_or_send_new_location_message(message)
        bot.register_next_step_handler(message, get_address)    

@with_locale
def get_address(message):
    user = BotUser.objects.filter(id=message.from_user.id).first()
    address_model = Address.objects.filter(user=user).first()
    all_addresses = AddressItem.objects.filter(base=address_model).all()

    if message.text == str(_('❌Cancel order')):
        messaging.let_us_start_from_the_beginning_message(message)
        messaging.back(message)
        bot.register_next_step_handler(message, on_command_specified)

    if message.content_type == 'location':
        coordinate1 = message.location.latitude
        coordinate2 = message.location.longitude
        coordinates = f"{coordinate1}, {coordinate2}"
        geolocator = Nominatim(user_agent="apps.bot")
        location = geolocator.reverse(coordinates)
        address = str(location.address)
        if not address_model:
            address_model = Address.objects.create(user=user)
        AddressItem.objects.create(base=address_model, address=address)
        messaging.deliver_location_message(message, address)
    
    for address in all_addresses:
        if message.text == str(address):
            messaging.deliver_location_message(message, address)

            