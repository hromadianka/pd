from django.shortcuts import render
import uuid
from .models import Publication
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html')

def publications(request):
    publications = Publication.objects.all()

    return render(request, 'publications.html', {'publications': publications})

def publication (request, pk):
    publication = Publication.objects.get(id=pk)

    return render(request, 'publication.html', {'publication': publication})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/publish')
        else:
            messages.error(request, 'Неправильно введені дані')
            return redirect('/signin')

    return render(request, 'signin.html')

@login_required(login_url='/signin')
def publish(request):
    if request.method == 'POST':
        heading = request.POST['heading']
        text = request.POST['text']
        image = request.FILES['image']

        publication = Publication.objects.create(heading=heading, text=text, image=image)
        publication.save()

        return redirect('/publications')

    return render(request, 'publish.html')