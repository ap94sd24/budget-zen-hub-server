from django.http import HttpResponse
from django.shortcuts import render

from .models import User

# Create your views here.
def activateemail(request):
  email = request.GET.get('email', '')
  id = request.GET.get('id', '')
  
  if email and id:
    user = User.objects.get(id=id, email=email)
    user.is_active = True
    user.save()
    
    print(user)
    
    return HttpResponse('The account is now activated. You can now go ahead and login!')
  else:
    return HttpResponse('The parameters are not valid!')