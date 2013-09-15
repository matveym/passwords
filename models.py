from google.appengine.ext import ndb


def init_localstore():
    from google.appengine.ext import testbed
    testbed = testbed.Testbed()
    testbed.activate()
    testbed.init_memcache_stub()
    testbed.init_datastore_v3_stub()


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