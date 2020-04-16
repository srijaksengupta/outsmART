from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from . import forms

@login_required
def info(request):
    return HttpResponse('Hello ' + request.user.username)


def signup(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
              user = User.objects.create_user(
                form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                )
              messages.success(request, 'Registration successful')
              return HttpResponseRedirect(reverse('account:login'))
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form   
    return render(request, 'account/signup.html', context)


def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                return redirect('pages:index')
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'account/login.html', context)


@login_required
def do_logout(request):
    logout(request)
    messages.success(request, 'Signed out successfully')
    return redirect('pages:index')

