from django.db import models
class Hospital(models.Model):
 name=models.CharField(max_length=200)
 city=models.CharField(max_length=100,default='Jaipur')
 address=models.TextField(blank=True)
 latitude=models.FloatField(null=True,blank=True)
 longitude=models.FloatField(null=True,blank=True)
 emergency_available=models.BooleanField(default=True)
 icu_beds=models.PositiveIntegerField(default=0)
 general_beds=models.PositiveIntegerField(default=0)
 capabilities=models.JSONField(default=list)
 def available_beds(self): return self.icu_beds+self.general_beds
