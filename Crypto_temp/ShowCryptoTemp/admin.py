from django.contrib import admin

from .models import *


admin.site.register(ShowCryptoTemp)
admin.site.register(Scrapper_bitcoin)
admin.site.register(Scrapper_Ethereum)
admin.site.register(Scrapper_doge)

# Register your models here.
