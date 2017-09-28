import grok

from zope.component import getUtility
from lovely.memcached.utility import MemcachedClient
from lovely.memcached.interfaces import IMemcachedClient


grok.global_utility(MemcachedClient, IMemcachedClient, direct=False)


def get_memcached_client():
    return getUtility(IMemcachedClient)


def cacheme(marshaller):

    def cache(func):

        def cache_replacement(*args, **kwargs):
            key = marshaller(func, *args, **kwargs)
            client = get_memcached_client()
            value = client.query(key, raw=False)
            if not value:
                value = func(*args, **kwargs)
                client.set(value, key, raw=False)
            return value
        return cache_replacement
    return cache


def invalidating(marshaller):
    def invalidate(func):
        def invalidate_replacement(*args, **kwargs):
            key = marshaller(func, *args, **kwargs)
            client = get_memcached_client()
            deleted = client.invalidate(key, raw=False)
            print "Deleted ", deleted
            return func(*args, **kwargs)
        return invalidate_replacement
    return invalidate
