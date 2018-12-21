from django.db import models

class Light(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    value = models.IntegerField()
    address = models.CharField(max_length=128)
    
    def __str__(self):
        return '(' + self.address + '):' +  str(self.value)
    
    class Meta:
        ordering = ['address', 'time']