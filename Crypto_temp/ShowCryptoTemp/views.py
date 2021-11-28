from django.http import HttpResponse, JsonResponse
from django.db.models import F
from django.shortcuts import render
from .models import *


def index(request):
    Bitcoin_temp_Query = ShowCryptoTemp.objects.filter(CryptoName= 'BitCoin')
    Ethereum_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='Ethereum')
    Doge_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='Doge')
    AdA_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='ADA')
    Ripple_temp_Query = ShowCryptoTemp.objects.filter(CryptoName='Ripple')

    Bitcoin_temp = float(Bitcoin_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    Ethereum_temp = float(Ethereum_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    Doge_temp = float(Doge_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    AdA_temp = float(AdA_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])
    Ripple_temp = float(Ripple_temp_Query.values('CryptoTemperture')[0]['CryptoTemperture'])


    context = {
        'Bitcoin_temp': Bitcoin_temp,
        'Ethereum_temp': Ethereum_temp,
        'Doge_temp': Doge_temp,
        'AdA_temp': AdA_temp,
        'Ripple_temp': Ripple_temp,
    }
    # return HttpResponse(Bitcoin_temp)
    return render(request,"ShowCryptoTemp/about.html",context)
