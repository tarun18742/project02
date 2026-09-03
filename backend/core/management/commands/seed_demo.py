from django.core.management.base import BaseCommand
from core.models import Hospital
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  data=[
   ('Sanjivni Jaipur Trauma & Emergency Centre','Jaipur',12,30,['trauma','cardiology','icu','emergency']),
   ('Sanjivni Pink City Multi-Speciality','Jaipur',8,24,['emergency','neurology','pediatrics'])
  ]
  for n,c,i,g,cap in data:
   Hospital.objects.update_or_create(name=n,defaults={'city':c,'icu_beds':i,'general_beds':g,'capabilities':cap})
  self.stdout.write(self.style.SUCCESS('Demo hospitals seeded.'))
