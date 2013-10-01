import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from google.appengine.api import users
from google.appengine.ext import ndb

from models import Site, root_key, site_key, all_sites
import settings
from utils import uniq


def home(request):
    current_user = users.get_current_user()
    if not current_user or not current_user.email() == 'slonenka@gmail.com':
        return redirect(users.create_login_url('/'))

    sites = all_sites()
    logins = sorted(uniq([site.login for site in sites if site.login]))
    passwords = sorted(uniq([site.password for site in sites if site.password]))
    return render(request, 'passwords.html', {
        'sites': sites,
        'sites_json': json.dumps(_sites_dict(sites)),
        'logins_json': json.dumps(logins),
        'passwords_json': json.dumps(passwords),
        'logout_url': users.create_logout_url('/'),
        })


def save_site(request):
    site_name =     request.POST.get('name')
    site_url =      request.POST.get('url')
    login =         request.POST.get('login')
    password =      request.POST.get('password')
    notes =         request.POST.get('notes')
    site_id =       request.POST.get('id')
    if site_id:
        site = site_key(site_id).get()
        site.name = site_name
        site.url = site_url
        site.login = login
        site.password = password
        site.notes = notes
        site.put()
    else:
        Site(name=site_name, url=site_url, login=login, password=password, notes=notes,
                parent=root_key).put()
    return HttpResponse(_refresh_sites(request))


def remove_site(request):
    site_id = request.POST['id']
    site_key(site_id).delete()
    return HttpResponse(_refresh_sites(request))


def upload(request):
    if request.method == 'POST':
        from tools import import_data
        data = request.POST['data']
        import_data(data)
        return redirect('/')
    return render(request, 'upload.html')


def _sites_dict(sites):
    sites_dict = {}
    for site in sites:
        sites_dict[site.id] = site.to_dict()
    return sites_dict


def _refresh_sites(request):
    sites = all_sites()
    sites_html = render(request, '_sites.html', {
        'sites': sites
        }).content

    logins = sorted(uniq([site.login for site in sites if site.login]))
    passwords = sorted(uniq([site.password for site in sites if site.password]))

    return json.dumps({
            'sites_html': sites_html,
            'sites': _sites_dict(sites),
            'logins': logins,
            'passwords': passwords,
            })
