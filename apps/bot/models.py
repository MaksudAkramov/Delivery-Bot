from django.db import models


from django.utils.translation import gettext_lazy as _



class BotUser(models.Model):
    class Locale(models.TextChoices):
        RU = 'ru', _("Russian")
        EN = 'en', _("English")
        UZ = 'uz', _("Uzbek")

        @classmethod
        def get_from_value(cls, value):
            value_dict = {
                _("Russian"): cls.RU,
                _("English"): cls.EN,
                _("Uzbek"): cls.UZ
            }
            return value_dict.get(value)

    id = models.BigIntegerField(verbose_name=_('ID'), primary_key=True)
    locale = models.CharField(max_length=2, default=Locale.RU, choices=Locale.choices)
    full_name = models.CharField(max_length=50, verbose_name=_('Full Name'), null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'), null=True, blank=True)
    is_admin = models.BooleanField(default=False)


    def __str__(self) -> str:
        return str(self.full_name)


class Address(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return str(self.user)

class AddressItem(models.Model):
    base = models.ForeignKey(Address, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, null=True)

    def __str__(self) -> str:
        return self.address