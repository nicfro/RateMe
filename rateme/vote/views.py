from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.forms import ModelForm

from vote.models import Image


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/vote/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class UploadImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ['uploaded', 'elo', 'user']


@login_required
def upload(request):
    success = False
    if request.method == 'POST':
        form = UploadImageForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            success = True
    else:
        form = UploadImageForm()
    return render(request, 'vote/upload.html', {'form': form, 'success': success})


@login_required
def vote(request):
    return render(request, 'vote/vote.html')
