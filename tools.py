from google.appengine.ext import ndb

from models import Site, init_localstore

def import_data():
    delete_all()

    lines = []
    with open('data.txt') as f:
        lines = f.readlines()
    for line in lines:
        try:
            site_name, login, password, notes = line.split(',')
        except ValueError:
            try:
                site_name, login, password = line.split(',')
                notes = ''
            except ValueError:
                site_name, password = line.split(',')
                login = ''
                notes = ''
        Site(name=site_name, url='', login=login, password=password, notes=notes).put()


def delete_all():
    keys = [site.key for site in Site.query()]
    ndb.delete_multi(keys)
