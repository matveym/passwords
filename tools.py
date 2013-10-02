from google.appengine.ext import ndb

from models import Site, root_key, all_sites


def import_file(name='data.txt'):
    lines = []
    with open(name) as f:
        lines = f.readlines()

    import_data(lines)


def read_file(name):
    with open(name) as f:
        return ''.join(f.readlines()).decode('utf8')


def parse_data(text):
    result = []
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
            site_name, login, password, notes = strip_all(site_name, login, password,
                    notes)
            result.append(Site(name=site_name, url='', login=login, password=password, notes=notes,
                parent=root_key))
    return result


def import_data(text):
    delete_all()

    for site in parse_data(text):
        site.put()


def delete_all():
    keys = [site.key for site in all_sites()]
    ndb.delete_multi(keys)
