from django.db import models
import datetime
import time
import arrow
# Create your models here.


class Expenses(models.Model):
    user = models.CharField( max_length=50)
    amount = models.IntegerField()
    category = models.CharField( max_length=50)
    desc = models.CharField(max_length=500)
    timestamp = models.DateField()
    def __str__(self):
        return "Rs {} in {} for {} on {}".format(self.amount, self.category, self.desc,(self.timestamp).strftime('%B %d, %Y'))
    def getCurrentMonth(user):
        return Expenses.getTransactions(user, datetime.datetime.now().month, datetime.datetime.now().year)
    def getPreviousMonth(user):
        month = datetime.datetime.now().month
        prevMonth = 12 if month == 1 else month - 1
        year = datetime.datetime.now().year
        prevYear = year - 1 if prevMonth == 12 else year
        return Expenses.getTransactions(user, prevMonth, prevYear)
    def getTransactions(user, month, year):
        return Expenses.objects.all().filter(user = user, timestamp__year = year, timestamp__month = month)
