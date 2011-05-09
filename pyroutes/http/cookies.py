#encoding: utf-8

import hmac
try:
    from hashlib import sha1
except ImportError:
    import sha as sha1

from pyroutes import settings

class RequestCookieHandler(object):
    """
    Class for handling all things regarding to cookies in pyroutes request
    objects.
    """

    def __init__(self, environ=None):
        if environ and 'HTTP_COOKIE' in environ:
            self._raw_cookies = dict(
                    [part.strip() for part in c.split('=', 1)]
                    for c in environ['HTTP_COOKIE'].split(';'))
        else:
            self._raw_cookies = {}

    def get_cookie(self, key):
        """
        Return a signed cookie value if it exists.
        """
        if key in self._raw_cookies:
            if '%s_hash' % key in self._raw_cookies:
                if settings.SECRET_KEY is None:
                    raise CookieKeyMissing(
                            'Set SECRET_KEY in settings to use cookies')
                cookie_hash = self._raw_cookies['%s_hash' % key]
                value_hash = hmac.HMAC(settings.SECRET_KEY, key +
                                       self._raw_cookies[key], sha1).hexdigest()
                if cookie_hash == value_hash:
                    return self._raw_cookies[key]
                else:
                    raise CookieHashInvalid(key, 'Cookie modified')
            else:
                raise CookieHashMissing(key, 'Cookie hash missing')
        else:
            return None

    def get_unsigned_cookie(self, key):
        """
        Return an unsigned cookie value. (Plain old-fashion cookie reading)
        """
        if key in self._raw_cookies:
            return self._raw_cookies[key]
        else:
            return None


class ResponseCookieHandler(object):
    """
    Handle cookie adding to request.
    """

    def __init__(self):
        self.cookie_headers = []

    def add_cookie(self, key, value, expires=None):
        if settings.SECRET_KEY is None:
            raise CookieKeyMissing('Set SECRET_KEY in settings to use cookies')
        cookie_hash = hmac.HMAC(settings.SECRET_KEY,
                                key + value, sha1).hexdigest()
        if expires:
            exp = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
            self.cookie_headers.append(
                ('Set-Cookie', '%s=%s; expires=%s' % (key, value, exp)))
            self.cookie_headers.append(
                ('Set-Cookie', '%s_hash=%s; expires=%s'
                    % (key, cookie_hash, exp)))
        else:
            self.cookie_headers.append(('Set-Cookie', '%s=%s' % (key, value)))
            self.cookie_headers.append(
                ('Set-Cookie', '%s_hash=%s' % (key, cookie_hash)))

    def add_unsigned_cookie(self, key, value, expires=None):
        if expires:
            exp = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
            self.cookie_headers.append(
                ('Set-Cookie', "%s=%s; expires=%s" % (key, value, exp)))
        else:
            self.cookie_headers.append(('Set-Cookie', "%s=%s" % (key, value)))

    def del_cookie(self, key):
        self.cookie_headers.append(
         ('Set-Cookie', "%s=null; expires=Thu, 01-Jan-1970 00:00:01 GMT" % key))
        self.cookie_headers.append(
         ('Set-Cookie', "%s_hash=null; expires=Thu, 01-Jan-1970 00:00:01 GMT"
            % key))

class CookieHashMissing(LookupError):
    pass

class CookieHashInvalid(ValueError):
    pass

class CookieKeyMissing(AttributeError):
    """Raised when SECRET_KEY is missing"""
