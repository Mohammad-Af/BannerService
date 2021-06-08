from django.db import models


# Create your models here.

class Click(models.Model):
    click_id = models.IntegerField()
    banner_id = models.IntegerField()
    campaign_id = models.IntegerField()
    quarter = models.IntegerField()

    class Meta:
        unique_together = ('click_id', 'quarter',)


class Impression(models.Model):
    banner_id = models.IntegerField()
    campaign_id = models.IntegerField()
    quarter = models.IntegerField()

    class Meta:
        unique_together = ('banner_id', 'campaign_id', 'quarter',)


class Conversion(models.Model):
    conversion_id = models.IntegerField()
    click_id = models.IntegerField()
    revenue = models.FloatField()
    quarter = models.IntegerField()

    class Meta:
        unique_together = ('conversion_id', 'quarter',)
