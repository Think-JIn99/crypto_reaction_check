from django.db import models

class ShowCryptoTemp(models.Model):
    CryptoName = models.CharField(max_length=200)
    CryptoTemperture = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return  self.CryptoName

class scrapper(models.Model):
    post_id = models.CharField(max_length=10)
    author = models.CharField(max_length=100)
    title = models.TextField()
    selftext = models.TextField()
    created_utc = models.IntegerField()
    num_comments = models.IntegerField()
    score = models.IntegerField()
    title_vader = models.FloatField()

    def __str__(self):
        return self.id
