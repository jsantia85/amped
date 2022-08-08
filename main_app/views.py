from django.shortcuts import render

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

class Gear:
  def __init__(self, name, brand, description, price):
    self.name = name
    self.brand = brand
    self.description = description
    self.price = price

gear = [
  Gear('Telecaster', 'Fender', 'Great for math rock.', 699),
  Gear('Stratocaster', 'Fender', 'Versitile, bright sounding.', 699),
  Gear('Audio Interface', 'BV', 'Affordable', 150),
  Gear('Chorus Pedal', 'Fender', 'Great modulator', 654)
]

def gear_index(request):
  return render(request, 'gear/index.html', {'gear': gear})