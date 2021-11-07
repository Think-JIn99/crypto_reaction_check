from django.db import models

class ShowCrypto(models.Model):
    CryptoName = models.CharField(max_length=200)
    CryptoTemperture = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
