import json

from django.http import HttpResponse
from django.shortcuts import render

from google.appengine.ext import ndb

from models import Site, init_localstore
import settings


if settings.DEBUG:
    init_localstore()


def home(request):
    sites = _all_sites()
    return render(request, 'passwords.html', {
        'sites': sites,
        'sites_json': json.dumps(_sites_dict(sites))
        })


def save_site(request):
    site_name =     request.POST.get('name')
    site_url =      request.POST.get('url')
    login =         request.POST.get('login')
    password =      request.POST.get('password')
    notes =         request.POST.get('notes')
    site_id =       request.POST.get('id')
    if site_id:
        site = ndb.Key('Site', int(site_id)).get()
        site.name = site_name
        site.url = site_url
        site.login = login
        site.password = password
        site.notes = notes
        site.put()
    else:
        Site(name=site_name, url=site_url, login=login, password=password, notes=notes).put()
    return HttpResponse(_refresh_sites(request))


def remove_site(request):
    site_id = request.POST['id']
    ndb.Key('Site', int(site_id)).delete()
    return HttpResponse(_refresh_sites(request))


def _sites_dict(sites):
    sites_dict = {}
    for site in sites:
        sites_dict[site.id] = site.to_dict()
    return sites_dict


def _refresh_sites(request):
    sites = _all_sites()
    sites_html = render(request, '_sites.html', {
        'sites': sites
        }).content

    return json.dumps({
            'sites_html': sites_html,
            'sites': _sites_dict(sites)
            })

def _all_sites():
    return list(Site.query().order(Site.key))
