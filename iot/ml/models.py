from django.db import models
from account.models import User

class Stock(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    x1 = models.FloatField()
    x2 = models.FloatField()
    x3 = models.FloatField()
    x4 = models.FloatField()
    x5 = models.FloatField()
    estimate = models.FloatField()
    
    def __str__(self):
        return '(' + self.date + ')'
    
    class Meta:
        ordering = ['date']


class Survive(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Age = models.FloatField()
    Embarked = models.IntegerField()
    Fare = models.FloatField()
    Pclass = models.IntegerField()
    Sex = models.IntegerField()
    Family_Size = models.IntegerField()
    Title2 = models.IntegerField()
    Ticket_info = models.IntegerField()
    Cabin = models.IntegerField()
    survive = models.IntegerField()
    
    def __str__(self):
        return '(' + str(self.Age) + ')' + str(self.Ticket_info)
    
    class Meta:
        ordering = ['id']