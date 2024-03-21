from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
def logins(request):
    if request.method == "POST":
         username=request.POST.get('u')
         password=request.POST.get('p')
         user = authenticate(username=username, password=password)
         print(user)
         if user is not None:
                login(request,user)
                return HttpResponse("HEllO")
                # return redirect('home')
         else:    
            # messages.error(request,"User did not exist please check your credentials")
            return redirect('r')
         
    return render(request,'login.html')

def register(request):
    if request.method =='POST':
        name=request.POST.get('u')
        email=request.POST.get('e')
        password=request.POST.get('p')
        
        if name is "" or email is ""  or password is "":
             return redirect('r')
        if User.objects.filter(username=name).exists():
            return HttpResponse("Username already exists!")
        # context={"k1":name, "k2":password}
        user = User.objects.create_user(
                    username=name,
                    email=email,
                    password=password
                )
        # user = authenticate(username=name, password=password)
        # login(request,user)
        subject = 'Welcome to our news website!'
        message = render_to_string('welcome_email.html', {'username': name})
        from_email = 'noreply.reachus@gmail.com'
        to_email = [user.email]
        send_mail(subject, '', from_email, to_email, html_message=message)
        return redirect('l')
    return render(request,'register.html')


