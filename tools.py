import csv
import codecs
import json
import StringIO

from google.appengine.ext import ndb

from models import Site, root_key, all_sites

def import_file(name='data.txt'):
    import_data(read_file(name))


def read_file(name):
    with open(name) as f:
        return ''.join(f.readlines()).decode('utf8')


def strip_all(*values):
    return [v.strip() for v in values]


def parse_data(text):
    result = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            site_name, url, login, password, notes = line.split(',')
        except ValueError:
            site_name, url, login, password = line.split(',')
            notes = ''
        site_name, login, password, notes = strip_all(site_name, login, password,
                notes)
        result.append(Site(name=site_name, url=url, login=login, password=password, notes=notes,
            parent=root_key))
    return result


def import_data(text):
    delete_all()

    for site in parse_data(text):
        site.put()

def export_to_csv():

    def to_csv_dict(site):
        return {
            "Account"       : site.name,
            "Login Name"    : site.login,
            "Password"      : site.password,
            "Web Site"      : site.url,
            "Comments"      : site.notes,
        }

    buf = StringIO.StringIO()
    writer = csv.DictWriter(buf,
            fieldnames=["Account","Login Name","Password","Web Site","Comments"]
        )
    writer.writeheader()
    for site in all_sites():
        writer.writerow({ k: v.encode('utf-8') for k, v in to_csv_dict(site).iteritems() })
    return buf.getvalue()


def delete_all():
    keys = [site.key for site in all_sites()]
    ndb.delete_multi(keys)
