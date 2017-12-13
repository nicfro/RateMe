from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    img = models.ImageField()
    elo = models.IntegerField(default=1500)

    uploaded = models.DateField(auto_created=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Elo(models.Model):
    img = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name="imgage")
    score = models.IntegerField()

    created = models.DateField(auto_created=True)


class Vote(models.Model):
    img_a = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name="img_a")
    img_b = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name="img_b")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created = models.DateField(auto_created=True)


class Report(models.Model):
    img = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
