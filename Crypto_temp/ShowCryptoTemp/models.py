from django.db import models


class ShowCryptoTemp(models.Model): # 크립토 온도 측정해서 보여주는 클래스
    CryptoName = models.CharField(max_length=200)
    CryptoTemperture = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.CryptoName


class scrapper(models.Model): # 스크래퍼
    post_id = models.CharField(max_length=10)
    title = models.TextField()
    created_utc = models.IntegerField(null=True)

    def __str__(self):
        return self.title
