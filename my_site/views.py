from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import QueryDict
from newsapi import NewsApiClient 
from itertools import islice
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

# def home(request):
#     newsapi = NewsApiClient(api_key ='e7bdc0e810624819986b94b0b02d0f1c') 
#     top = newsapi.get_top_headlines(country ='in')  
  
#     l = top['articles']
#     desc =[] 
#     news =[] 
#     img =[] 
#     urls = []
#     for i in range(len(l)): 
#         f = l[i] 
#         news.append(f['title']) 
#         desc.append(f['description']) 
#         img.append(f['urlToImage']) 
#         urls.append(f['url'])
#     mylist = zip(news, desc, img,urls)
#     # mylist = list(islice(zip(news, desc, img, urls), 100))  
#     # mylist = [(f['title'], f['description'], f['urlToImage'], f['url']) for f in l[:100]]
#     # print(len(mylist))
#     # print(top)
#     return render (request,'index.html',context ={"mylist":mylist})


def logouts(request):
    logout(request)
    return redirect('l')

def feedback(request):
    return render(request,'form.html')

def home(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
        newsapi = NewsApiClient(api_key='e7bdc0e810624819986b94b0b02d0f1c')
        top = newsapi.get_everything(q=search_text, language='en', sort_by='relevancy')

        l = top['articles']
        desc = []
        news = []
        img = []
        urls = []
        for i in range(len(l)):
            f = l[i]
            news.append(f['title'])
            desc.append(f['description'])
            img.append(f['urlToImage'])
            urls.append(f['url'])
        mylist = zip(news, desc, img, urls)
    else:
        # Display default news (e.g., top headlines from India)
        newsapi = NewsApiClient(api_key='e7bdc0e810624819986b94b0b02d0f1c')
        top = newsapi.get_top_headlines(country='in')

        l = top['articles']
        desc = []
        news = []
        img = []
        urls = []
        for i in range(len(l)):
            f = l[i]
            news.append(f['title'])
            desc.append(f['description'])
            img.append(f['urlToImage'])
            urls.append(f['url'])
        mylist = zip(news, desc, img, urls)

    context = {"mylist": mylist}
    return render(request, 'index.html', context)

def submit(request):
    if request.method =="POST":
        return render(request,'form')
    

def tech(request):
    newsapi = NewsApiClient(api_key='e7bdc0e810624819986b94b0b02d0f1c') 
    top = newsapi.get_top_headlines(category='sports')

    articles = top['articles']
    news = []
    desc = []
    img = []
    urls = []
    for article in articles:
        news.append(article['title'])
        desc.append(article['description'])
        img.append(article['urlToImage'])
        urls.append(article['url'])

    mylist = zip(news, desc, img, urls)

    return render(request, 'index.html', context={"mylist": mylist})

def business(request):
    newsapi = NewsApiClient(api_key='e7bdc0e810624819986b94b0b02d0f1c') 
    top = newsapi.get_top_headlines(category='business') 

    articles = top['articles']
    news = []
    desc = []
    img = []
    urls = []
    for article in articles:
        news.append(article['title'])
        desc.append(article['description'])
        img.append(article['urlToImage'])
        urls.append(article['url'])

    mylist = zip(news, desc, img, urls)

    return render(request, 'index.html', context={"mylist": mylist})

def enter(request):
    newsapi = NewsApiClient(api_key='e7bdc0e810624819986b94b0b02d0f1c') 
    top = newsapi.get_top_headlines(category='entertainment')  
    articles = top['articles']
    news = []
    desc = []
    img = []
    urls = []
    for article in articles:
        news.append(article['title'])
        desc.append(article['description'])
        img.append(article['urlToImage'])
        urls.append(article['url'])

    mylist = zip(news, desc, img, urls)

    return render(request, 'index.html', context={"mylist": mylist})
 
def science(request):
    newsapi = NewsApiClient(api_key='e7bdc0e810624819986b94b0b02d0f1c') 
    top = newsapi.get_top_headlines(category='science')  
    articles = top['articles']
    news = []
    desc = []
    img = []
    urls = []
    for article in articles:
        news.append(article['title'])
        desc.append(article['description'])
        img.append(article['urlToImage'])
        urls.append(article['url'])

    mylist = zip(news, desc, img, urls)

    return render(request, 'index.html', context={"mylist": mylist})
 
 
 
 