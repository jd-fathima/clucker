"""Views of the microblogs app."""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from .forms import LogInForm, PostForm, SignUpForm
from .models import Post, User
from .helpers import login_prohibited

@login_required
def feed(request):
    form = PostForm()
    current_user = request.user
    authors = list(current_user.followees.all()) + [current_user]
    posts = Post.objects.filter(author__in=authors)

    return render(request, 'feed.html', {'form': form, 'user':current_user, 'posts': posts})

@login_required
def follow_toggle(request, user_id):
    current_user = request.user
    try:
        followee = User.objects.get(id=user_id)
        current_user.toggle_follow(followee)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return redirect('show_user', user_id=user_id)

@login_required
def follow_toggle(request, user_id):
    current_user = request.user
    try:
        followee = User.objects.get(id=user_id)
        current_user.toggle_follow(followee)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return redirect('show_user', user_id=user_id)

class LogInView(View):
    """View that handles log in """

    http_method_names = ['get', 'post']

    @method_decorator(login_prohibited)
    def dispatch(self, request):
        return super().dispatch(request)

    def get(self, request):
        """Display log in template"""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt"""
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in templaate with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})



# @login_prohibited
# def log_in(request):
#     if request.method == 'POST':
#         form = LogInForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 redirect_url = request.POST.get('next') or 'feed'
#                 return redirect(redirect_url)
#         messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
#     else:
#         next = request.GET.get('next') or ''
#     form = LogInForm()
#     return render(request, 'log_in.html', {'form': form, 'next': next})

def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required
def show_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user)
        following = request.user.is_following(user)
        followable = (request.user != user)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return render(request, 'show_user.html',
        {'user': user,
        'posts': posts,
        'following': following,
        'followable':followable}
        ) # posts gets passed onto templates

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def new_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            current_user = request.user
            form = PostForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                post = Post.objects.create(author=current_user, text=text)
                return redirect('feed')
            else:
                return render(request, 'feed.html', {'form': form})
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden()
