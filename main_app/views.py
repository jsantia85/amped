from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Gear

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

def gear_index(request):
  gear = Gear.objects.filter(user=request.user)
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('gear_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)