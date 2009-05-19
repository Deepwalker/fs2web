from django.db import models as m

# Create your models here.

class Conference(m.Model):
    name = m.CharField("Name",max_length=254)
