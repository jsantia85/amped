from django.db import models
from django.urls import reverse

class Gear(models.Model):
  name = models.CharField(max_length=100)
  brand = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  price = models.IntegerField()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("gear_detail", kwargs={"gear_id": self.id})
