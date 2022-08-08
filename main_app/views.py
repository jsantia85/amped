from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Gear

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def gear_index(request):
  gear = Gear.objects.all()
  return render(request, 'gear/index.html', {'gear': gear})

def gear_detail(request, gear_id):
  gear = Gear.objects.get(id=gear_id)
  return render(request, 'gear/detail.html', { 'gear': gear})

class GearCreate(CreateView):
  model = Gear
  fields = ['name', 'brand', 'description', 'price']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class GearUpdate(UpdateView):
  model = Gear
  fields = ['brand', 'description', 'price']

class GearDelete(DeleteView):
  model = Gear
  success_url = '/gear/'