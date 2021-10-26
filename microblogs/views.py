from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, PostForm


# Create your views here.
def show_user(request):



def user_list(request):
    User = get_user_model()
    list = User.objects.all()
    return render(request, 'user_list.html', {"list": list})

#display a Post
def feed(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'feed.html',{'form': form})

def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        form.printText()
    else:
        form = PostForm()
    return render(request, 'post.html',{'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)#checks the values and checks if it is active too
            if user is not None: #have been given a user object
                login(request, user)
                return redirect('feed')
            #add error message here
            messages.add_message(request,messages.ERROR, "The credientials provided were invalid!!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()#record has been safe
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
