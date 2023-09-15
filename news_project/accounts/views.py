from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Mufaqqiyatli login amalga oshirildi>')
                else:
                    return HttpResponse('Sizning profilingiz actice holatda emas')

            return HttpResponse('Login va parolda xatolik bor')

    else:
        form = LoginForm()
        context={
            'form':form
        }
    return render(request, 'registration/login.html', context)




# Create your views here.
