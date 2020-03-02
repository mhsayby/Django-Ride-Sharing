from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SearchForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return render(request, 'users/user_status.html')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@login_required
def car_status(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return user_driver(request)
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'users/car_info.html', context)


@login_required
def user_status(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return render(request, 'users/user_status.html')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }

    return render(request, 'users/person_info.html', context)


@login_required
def search(request):
    if request.method == 'POST':
        s_form = SearchForm(request.POST,
                            request.FILES,
                            instance=request.user.profile)
        if s_form.is_valid():
            s_form.save()
            return render(request, 'rides/search_confirm.html')
    else:
        s_form = SearchForm(instance=request.user)

    context = {
        's_form': s_form
    }

    return render(request, 'users/search.html', context)


@login_required
def user_driver(request):
    if request.user.profile.type == '' or request.user.profile.plate == '' or request.user.profile.volume == '':
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'p_form': p_form
        }

        return render(request, 'users/car_info.html', context)
    else:
        request.user.profile.status = "driver"
        request.user.profile.save()
        context = {
            'content': "driver",
        }
        return render(request, 'users/user_status.html', context)


@login_required
def user_owner(request):
    request.user.profile.status = "owner"
    request.user.profile.save()
    context = {
        'content': "owner"
    }

    return render(request, 'users/user_status.html', context)


@login_required
def user_sharer(request):
    request.user.profile.status = "sharer"
    request.user.profile.save()
    context = {
        'content': "sharer"
    }

    return render(request, 'users/user_status.html', context)