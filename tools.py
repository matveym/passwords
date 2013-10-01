from google.appengine.ext import ndb

from models import Site, root_key


def import_file():
    lines = []
    with open('data.txt') as f:
        lines = f.readlines()

    import_data(lines)


def import_data(text):
    delete_all()

    for line in text.splitlines():
        line = line.strip()
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
        Site(name=site_name, url='', login=login, password=password, notes=notes,
                parent=root_key).put()


def delete_all():
    keys = [site.key for site in Site.query()]
    ndb.delete_multi(keys)
