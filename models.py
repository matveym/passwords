import json

from google.appengine.ext import ndb


class SiteRoot(ndb.Model):
    pass


def get_site_root_key():
    roots = list(SiteRoot.query())
    assert len(roots) in [0, 1], roots

    if not roots:
        root_key = SiteRoot().put()
    else:
        root_key = roots[0].key
    return root_key

root_key = get_site_root_key()


class Site(ndb.Model):
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    login = ndb.StringProperty()
    # TODO Make BlobProperty, encrypt
    password = ndb.StringProperty()
    notes = ndb.StringProperty()

    @property
    def id(self):
        if not self.key:
            return None
        return self.key.id()

    @property
    def href(self):
        if self.url.startswith('http'):
            return self.url
        else:
            return '//' + self.url

    def to_dict(self):
        return {
        'id':       self.id,
        'name':     self.name,
        'url':      self.url,
        'login':    self.login,
        'password': self.password,
        'notes':    self.notes
        }

    @property
    def json(self):
        return json.dumps(self.to_dict())


def site_key(site_id):
    return ndb.Key(root_key.kind(), root_key.id(), 'Site', int(site_id))


def all_sites():
    return list(Site.query(ancestor=root_key).order(Site.name))
