from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Gear, Photo
import uuid
import boto3


S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'jsamped'

class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def gear_index(request):
  gear = Gear.objects.filter(user=request.user)
  return render(request, 'gear/index.html', {'gear': gear})

@login_required
def gear_detail(request, gear_id):
  gear = Gear.objects.get(id=gear_id)
  return render(request, 'gear/detail.html', { 'gear': gear})

class GearCreate(LoginRequiredMixin, CreateView):
  model = Gear
  fields = ['name', 'brand', 'description', 'price']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class GearUpdate(LoginRequiredMixin, UpdateView):
  model = Gear
  fields = ['brand', 'description', 'price']

class GearDelete(LoginRequiredMixin, DeleteView):
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

def add_photo(request, gear_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      photo = Photo(url=url, gear_id=gear_id)
      # Remove old photo if it exists
      gear_photo = Photo.objects.filter(gear_id=gear_id)
      if gear_photo.first():
        gear_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('gear_detail', gear_id=gear_id)