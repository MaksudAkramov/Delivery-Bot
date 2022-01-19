from django.contrib import admin

from apps.bot.models import Address, AddressItem, BotUser


admin.site.register(BotUser)
admin.site.register(Address)
admin.site.register(AddressItem)
