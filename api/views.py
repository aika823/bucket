

from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from requests.models import Response
from user.forms import LoginForm
from user.models import User


def login(request):
    print(request)
    if request.method == 'POST':
        name = request.POST.get('name')
        password = make_password(request.POST.get('password'))
        print(name)
        print(password)
        try: 
            user = User.objects.get(name=name, password=password)
            return redirect('user:profile', {'user':user})
        except:
            return redirect('user:login')
            
            
        # name = User.objects.filter(id=form.user_id).values('name')[0]['name']
        # image_src = str(User.objects.filter(id=form.user_id).values('image')[0]['image'])
        # return redirect('user:profile')
        # return render(request, 'home.html', {'name':name, 'image_src':image_src})
