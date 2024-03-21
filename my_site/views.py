from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import QueryDict
def logins(request):
    username = request.GET.get('u', '') 
    if request.method == "POST":
         username=request.POST.get('u')
         password=request.POST.get('p')
         user = authenticate(username=username, password=password)
         if user is not None:
            user_agent = request.user_agent
            browser = user_agent.browser.family
            os = user_agent.os.family
            is_pc = user_agent.is_pc

           
            subject = 'Login Notification'
            message = f'Hello {user.username},\n\nYou have successfully logged in to our website.\n\nBrowser: {browser}\nOperating System: {os}\nDevice Type: {"PC" if is_pc else "Mobile"}'
            from_email = 'noreply.reachus@gmail.com'  
            to_email = [user.email]  
        
            send_mail(subject, message, from_email, to_email)
            login(request,user)
            return redirect('h')
         else:    
            # messages.error(request,"User did not exist please check your credentials")
            return redirect('r')
         
    return render(request,'login.html',{'username': username})

def register(request):
    if request.method =='POST':
        name=request.POST.get('u')
        email=request.POST.get('e')
        password=request.POST.get('p')
        
        if name is "" or email is ""  or password is "":
             return redirect('r')
        if User.objects.filter(username=name).exists():
            return HttpResponse("Username already exists!")
        user = User.objects.create_user(
                    username=name,
                    email=email,
                    password=password
                )
        subject = 'Welcome to our news website!'
        message = render_to_string('welcome_email.html', {'username': name})
        from_email = 'noreply.reachus@gmail.com'
        to_email = [user.email]
        send_mail(subject, '', from_email, to_email, html_message=message)
        return redirect(f'/login?u={name}')
    return render(request,'register.html')

def home(request):
     return render (request,'index.html')

