from django.http import HttpResponse
from django.shortcuts import render


from models import Site, init_localstore
import settings


if settings.DEBUG:
    init_localstore()


def home(request):
    return render(request, 'passwords.html', {
        'sites': _all_sites()
        })


def add_site(request):
    site_name = request.POST['name']
    site_url = request.POST.get('url')
    login = request.POST['login']
    password = request.POST['password']
    notes = request.POST.get('notes')

    Site(name=site_name, url=site_url, login=login, password=password, notes=notes).put()
    return render(request, '_sites.html', {
        'sites': _all_sites()
        })


def _all_sites():
    return list(Site.query().order(Site.key))
