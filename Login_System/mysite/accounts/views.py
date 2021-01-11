from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, FormView, TemplateView
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterationForm, GuestForm
# from .models import GuestEmail


class HomeView(TemplateView):
    template_name = 'home.html'

# @login_required
# def home(request):
#     return render(request, "home.html")


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}

    if request.POST:
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:  # if destination != None
                return redirect(destination)
            return redirect("home")

        else:
            context['registeration_form'] = form

    else:
        form = RegisterationForm()
        context['registeration_form'] = form

    return render(request, 'LoginModal/register.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "logout successfully",
                     "alert alert-success alert-dismissible fade show")
    return redirect("home")


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
        return redirect

# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'login.html'
#     success_url = '/login/'


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        messages.success(request, f"You are already logged in as {user}",
                         "alert alert-success alert-dismissible fade show")
        return redirect("home")
    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "loged in successfully",
                                 "alert alert-success alert-dismissible fade show")
                if destination:
                    return redirect(destination)
                return redirect("home")
    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request, "LoginModal/login.html", context)

# class LoginView(FormView):
#     form_class = LoginForm
#     success_url = '/'
#     template_name = 'User.html'

#     def post(self, request):
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(email=email, password=password)

#         if user is not None:
#             if user.is_active:
#                 login(request, user)

#                 return HttpResponseRedirect('/')
#             else:
#                 return HttpResponse("Inactive user.")
#         else:
#             return HttpResponseRedirect(settings.LOGIN_URL)

#         return render(request, "index.html")

# @login_required
# @transaction.atomic


def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _(
                'Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
