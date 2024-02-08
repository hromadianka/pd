from django.shortcuts import render
import uuid
from .models import Publication
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils.html import strip_tags
from django.db.models import Q
import locale

# locale.setlocale(
#     category=locale.LC_ALL,
#     locale="Ukrainian"
# )

def ukr_month_str(date):
    ukr_months = ['січень', 'лютий', 'березень', 'квітень', 'травень', 'червень', 'липень', 'серпень',
                  'вересень', 'жовтень', 'листопад', 'грудень']
    return ukr_months[date.month - 1]

def legible_date(date):
    res = date.strftime("%B %d, %Y")
    month_word_end = res.find(' ')
    return ukr_month_str(date) + res[month_word_end:]

def str_list_topics(topics_from_db):
    TOPICS = ['news', 'theory', 'protests']
    TOPICS2STR = {'news': 'новини', 'theory': 'теорія', 'protests': 'протести'}
    return list(map(lambda x: TOPICS2STR[x], filter(lambda x: x in TOPICS, map(str.strip, topics_from_db.split(',')))))

def str_topics(topics_from_db):
    return ", ".join(str_list_topics(topics_from_db))

# Create your views here.

def index(request):
    publications = Publication.objects.all()

    publications_by_date = sorted(list(filter(lambda x: x.date is not None, publications)), key=lambda x: x.date, reverse=True)

    for p in publications_by_date:
        if type(p.text) == bytes:
            p.text = strip_tags(p.text.decode('utf-8'))
        p.date_legible = legible_date(p.date)

    latest_publication = publications_by_date[0]
    publications_by_date = publications_by_date[1:4]

    return render(request, 'index.html', {'latest_topic': latest_publication, 'latest_topics': publications_by_date})

def publications(request):
    publications = None
    search_publication = request.GET.get('search')
    if search_publication:
        publications = Publication.objects.filter(Q(heading__icontains=search_publication) | Q(text__icontains=search_publication))
    else:
        publications = Publication.objects.all()

    publications = sorted(list(filter(lambda x: x.date is not None, publications)), key=lambda x: x.date, reverse=True)

    for p in publications:
        if type(p.text) == bytes:
            p.text = p.text.decode('utf-8')
        p.date_legible = legible_date(p.date)
        p.topics_legible = str_topics(p.topics)

    test_pubs = []
    i = 0
    for p in publications:
        print(i)
        if i == 0:
            print('+')
            test_pubs.append([])
        test_pubs[-1].append(p)
        i = (i + 1) % 3

    

    return render(request, 'publications.html', {'publications': test_pubs})





def publication(request, pk):
    # publication = Publication.objects.get(id=pk)
    
    # SAMODEL
    publications = Publication.objects.all()
    publication = None
    for p in publications:
        if uuid.UUID(pk) == p.id: publication = p

    if type(publication.text) == bytes:
        publication.text = publication.text.decode('utf-8')
        publication.date_legible = legible_date(publication.date)

    return render(request, 'publication.html', {'publication': publication})

def materials(request):
    return render(request, 'materials.html')

def branches(request):
    return render(request, 'branches.html')

def game(request):
    return render(request, 'game.html')

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
        
        # Перевіряємо, чи вибраний файл у формі
        if 'image' in request.FILES:
            image = request.FILES['image']
            publication = Publication.objects.create(heading=heading, text=text, image=image)
        else:
            publication = Publication.objects.create(heading=heading, text=text)
        
        publication.save()

        return redirect('/publications')

    return render(request, 'publish.html')
