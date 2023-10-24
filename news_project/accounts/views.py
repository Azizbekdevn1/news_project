from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .forms import LoginForm,UserRegistrationForm
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserUpdateFrom,ProfileUpdateFrom

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
    return render(request, 'registration/login.html', {'form': form})

def dashboard_view(request):
    user = request.user
    context={
        'user':user
    }
    return render(request,'pages/user_profile.html', context)

#0 dan qolda yozildi
def user_register(request):
    if request.method == 'POST':
        user_form =UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context={
                "new_user":new_user
            }
            return render(request, 'account/register_done.html', context)
        return HttpResponse("User registered successfully!")

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form':user_form})

#Tayyor django Createtion formdan foydalanib yaratildi
class SignUpView(CreateView):
   form_class = UserCreationForm
   success_url = reverse_lazy('login')
   template_name = 'account/register.html'


def Edit_user(request):
    if request.method =='POST':
        user_form =UserUpdateFrom(instance=request.user,data=request.POST)
        profile_form=ProfileUpdateFrom(instance=request.user.profile,data=request.POST,
                                       files=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form=UserUpdateFrom(instance=request.user)
        profile_form=ProfileUpdateFrom(instance=request.user.profile)
    return render(request,'account/profile_edit.html',{'user_form':user_form,'profile_form':profile_form})
