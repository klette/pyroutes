# encoding: utf-8

import cgi
import os

from pyroutes.http.cookies import RequestCookieHandler

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

class Request(object):
    """
    The pyroutes Request object. Contains all information about a request, like
    GET/POST and environment data.
    """

    def __init__(self, environment):
        self.GET = {}
        self.POST = {}
        self.PUT = {}
        self.FILES = {}
        self.ENV = environment

        self.GET = self.extract_get_data(environment)
        self.POST = self.extract_post_data(environment)
        self.PUT = self.extract_put_data(environment)

        self.COOKIES = RequestCookieHandler(environment)
        self.params = {}

    def __repr__(self):
        values = (self.GET, self.POST, self.PUT, self.COOKIES._raw_cookies,
                  self.FILES.keys())
        return "GET: %s\nPOST: %s\nPUT: %s\nCOOKIES: %s\nFILES: %s" % values

    def extract_put_data(self, environment):
        '''Extracts the file pointer from a PUT request.

        The PUT method allows you to write the contents of the file to the
        socket connection that is established with the server directly.

        According to the [HTTP/1.1 specification (RFC2616)][0], the server must
        return a status code of 201 (Created) if the file in question is newly
        created, and 200 (OK) or 204 (No Content) if the request results in a
        successful update.

        When using the POST method, all the fields and files are combined into a
        single multipart/form-data type object, and this has to be decoded by
        the server side handler.

        [0]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html

        '''
        if environment.get('REQUEST_METHOD', 'GET') == 'PUT':
            if hasattr(environment['wsgi.input'], 'read'):
                return environment['wsgi.input']

        return None

    def extract_post_data(self, environment):
        data = {}

        # Copy enviroment so we dont get GET-variables in the result.
        env = environment.copy()
        env['QUERY_STRING'] = ''

        if env.get('REQUEST_METHOD', 'GET') == 'POST':
            _data = cgi.FieldStorage(
                fp=environment['wsgi.input'],
                environ=env,
                keep_blank_values=False
            )
            for key in _data.keys():
                value = self._parse_field(_data[key], key, _data)
                if value is not None:
                    self._assign_field_to_section(key, value, data)

        return data

    def extract_get_data(self, environment):
        ret_dict = {}
        for (key, value) in cgi.parse_qsl(environment.get('QUERY_STRING', '')):
            if key in ret_dict:
                if not isinstance(ret_dict[key], list):
                    ret_dict[key] = [ret_dict[key]]
                ret_dict[key].append(value)
            else:
                ret_dict[key] = value
        return ret_dict

    def _assign_field_to_section(self, key, value, storage):
        if isinstance(value, list):
            for val in value:
                self._assign_field_to_section(key, val, storage)
        else:
            if isinstance(value, tuple) and value[1] and \
              (isinstance(value[1], file) or  hasattr(value[1], 'read')):

                # If an existing value exists for this key, convert to
                # list-result
                if key in self.FILES and not isinstance(self.FILES[key], list):
                    self.FILES[key] = [self.FILES[key]]

                if key in self.FILES and isinstance(self.FILES[key], list):
                    self.FILES[key].append(value)
                else:
                    self.FILES[key] = value
            elif isinstance(value, basestring):
                # If an existing value exists for this key, convert to
                # list-result
                if key in storage and not isinstance(storage[key], list):
                    storage[key] = [storage[key]]

                if key in storage and isinstance(storage[key], list):
                    storage[key].append(value)
                else:
                    storage[key] = value

    def _parse_field(self, field, key, data):
        value = None
        if isinstance(field, list):
            value = [self._parse_field(f, key, data) for f in field]
        if hasattr(field, 'filename') and field.filename:
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
