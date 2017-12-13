from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.forms import ModelForm

from vote.models import Image, Vote


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
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


def updateScore(winner, loser, tie, k):
    EA = (1 / (1 + 10 ** ((loser - winner) / 400)))
    EB = (1 / (1 + 10 ** ((winner - loser) / 400)))

    if tie == 0:
        winner = winner + k * (1 - EA)
        loser = loser + k * (0 - EB)
    else:
        winner = winner + k * (0.5 - EA)
        loser = loser + k * (0.5 - EB)

    return winner, loser


def contenders(user):
    return Image.objects.order_by("?")[:2]




@login_required
def vote(request):
    if request.method == "POST":
        vote = Vote()
        vote.img_a = Image.objects.get(pk=request.POST["img_a"])
        vote.img_b = Image.objects.get(pk=request.POST["img_b"])
        vote.user = request.user
        vote.winner = Image.objects.get(pk=request.POST["winner"])
        vote.save()

    img_a, img_b = contenders(request.user)

    return render(request, 'vote/vote.html', {"img_a": img_a, "img_b": img_b})
