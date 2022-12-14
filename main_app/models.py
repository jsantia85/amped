from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Gear(models.Model):
  name = models.CharField(max_length=100)
  brand = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  price = models.IntegerField()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("gear_detail", kwargs={"gear_id": self.id})

  user = models.ForeignKey(User, on_delete=models.CASCADE)

class Photo(models.Model):
  url = models.CharField(max_length=250)
  gear = models.OneToOneField(Gear, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for gear_id: {self.gear_id} @{self.url}"