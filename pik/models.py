from django.db import models


class Fitting(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField(null=True)


class FittingNeck(models.Model):
    fitting = models.ForeignKey(Fitting, on_delete=models.CASCADE)
    diameter = models.IntegerField()
    CHOICES = (
        ('male', 'Папа'),
        ('female', 'Мама'),
    )
    type = models.CharField(max_length=10, choices=CHOICES)
