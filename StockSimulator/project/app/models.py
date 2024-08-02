from django.contrib.auth.models import User
from django.db import models

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=64, default="Listing Title")
    price = models.DecimalField(max_digits=16, decimal_places=2)
    volatility = models.DecimalField(decimal_places=4, max_digits=16)
    annualchange = models.DecimalField(decimal_places=4, max_digits=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=64, default="Listing Title")
    strength = models.DecimalField(max_digits=16, decimal_places=4)
    decay_rate = models.DecimalField(max_digits=16, decimal_places=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class StockInPortfolio(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)