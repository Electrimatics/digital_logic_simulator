from django.db import models

# Create your models here.

#This would probably be changed later to suit our needs.
class LogicGate(models.Model):
    gate_type = models.TextField() #Type stored as textfield
    image_url = models.TextField() #Image stored as textfield for now (need image links)
