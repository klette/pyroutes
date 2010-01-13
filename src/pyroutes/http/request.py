# encoding: utf-8

import cgi
import hmac
import base64

from pyroutes import settings
from pyroutes.http.cookies import RequestCookieHandler

try:
    from hashlib import sha1
except ImportError:
    import sha as sha1

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

class Request(object):

    def __init__(self, environment):
        self.ERRORS = []
        self.ENV = environment

        # Initialize GET
        self.GET = self.get_GET_data(environment)

        # Initialize POST and FILES
        self.POST = {}
        self.FILES = {}
        self.get_POST_data(environment)

        self.COOKIES = RequestCookieHandler(environment)


    def __repr__(self):
        return "GET: %s\nPOST: %s\nCOOKIES: %s\nFILES: %s" % (self.GET, self.POST,self.COOKIES._raw_cookies, self.FILES.keys())

    def get_POST_data(self, environment):
        data = {}

        # Copy enviroment so we dont get GET-variables in the result.
        env = environment.copy()
        env['QUERY_STRING'] = ''

        if env.get('REQUEST_METHOD', 'GET') == 'POST':
            length = int(env.get('CONTENT_LENGTH', 0))
            input_buffer = StringIO.StringIO()
            read_bytes = 1024*32
            while length:
                if read_bytes > length:
                    read_bytes = length
                input_buffer.write(environment['wsgi.input'].read(read_bytes))
                length = length - read_bytes
                if length < 0:
                    length = 0

            input_buffer.reset()

            _data = cgi.FieldStorage(
                fp=input_buffer,
                environ=env,
                keep_blank_values=False
            )
            for key in _data.keys():
                value = self._parse_field(_data[key], key, _data)
                if value is not None:
                    self._assign_field_to_section(key, value)

            input_buffer.close()
        return data

    def get_GET_data(self, environment):
        return dict(cgi.parse_qsl(environment.get('QUERY_STRING', '')))

    def _assign_field_to_section(self, key, value):
        if isinstance(value, list):
            for v in value:
                self._assign_field_to_section(key, v)
        else:
            if isinstance(value, tuple) and value[1] \
                and (isinstance(value[1], file) or  hasattr(value[1], 'read')):
                # ^^^ FIXME: Yuk. Find a better way.

                # If an existing value exists for this key, convert to list-result
                if key in self.FILES and not isinstance(self.FILES[key], list):
                    self.FILES[key] = [self.FILES[key]]

                if key in self.FILES and isinstance(self.FILES[key], list):
                    self.FILES[key].append(value)
                else:
                    self.FILES[key] = value
            elif isinstance(value, basestring):
                # If an existing value exists for this key, convert to list-result
                if key in self.POST and not isinstance(self.POST[key], list):
                    self.POST[key] = [self.POST[key]]

                if key in self.POST and isinstance(self.POST[key], list):
                    self.POST[key].append(value)
                else:
                    self.POST[key] = value

    def _parse_field(self, field, key, data):
        value = None
        if isinstance(field, list):
            value = [self._parse_field(f, key, data) for f in field]
        if field.filename:
            if field.file:
                value = (field.filename, field.file)
            else:
                value = (field.filename, StringIO.StringIO(data.getvalue(key)))
        else:
            if isinstance(data.getvalue(key), basestring):
                try:
                    value = unicode(data.getvalue(key), 'utf-8')
                except UnicodeDecodeError:
                    # If we can't understand the data as utf, try latin1
                    value = unicode(data.getvalue(key), 'iso-8859-1')

        return value
