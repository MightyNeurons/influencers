from django.db import models

# Create your models here.

class Offer_Details(models.Model):
    Proof_Url = models.URLField()
    Proof_Url_Scnd = models.URLField(blank=True)
    Proof_Url_Third = models.URLField(blank=True)


class Earned_by_Freelancer(models.Model):
    Money_Reciever = models.IntegerField()
    Money_Releser = models.IntegerField()
    Value = models.IntegerField(blank=True, default=0)
    Date_Created = models.DateField(auto_now_add=True)


