# encoding: utf-8

"""
This module contains only the Request class, a key class in pyroutes. Request
objects hold all meta about incoming requests.
"""

from cgi import parse_qsl, FieldStorage

from pyroutes.http.cookies import RequestCookieHandler

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class Request(object):
    """
    The pyroutes Request object.
    Contains all information about a request,
    like GET/POST and environment data.
    """

    def __init__(self, environment):
        self.GET = {}
        self.POST = {}
        self.PUT = {}
        self.FILES = {}
        self.ENV = environment

        self.extract_get_data()
        self.extract_post_data()
        self.extract_put_data()

        self.COOKIES = RequestCookieHandler(environment)
        self.params = {}

        self.matched_path = None

    def __repr__(self):
        values = (self.GET, self.POST, self.PUT, self.COOKIES,
                  self.FILES.keys())
        return "GET: %s\nPOST: %s\nPUT: %s\nCOOKIES: %s\nFILES: %s" % values

    def extract_put_data(self):
        """Extracts the file pointer from a PUT request.

        The PUT method allows you to write the contents of the file to the
        socket connection that is established with the server directly.

        According to the [HTTP/1.1 specification (RFC2616)][0], the server
        must return a status code of 201 (Created) if the file in question
        is newly created, and 200 (OK) or 204 (No Content) if the request
        results in a successful update.

        When using the POST method, all the fields and files are combined
        into a single multipart/form-data type object, and this has to be
        decoded by the server side handler.

        [0]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html

        """
        if self.ENV.get('REQUEST_METHOD', 'GET') == 'PUT':
            if hasattr(self.ENV['wsgi.input'], 'read'):
                self.PUT = self.ENV['wsgi.input']

    def extract_post_data(self):
        "Populates the POST variable"
        data = {}

        # Copy enviroment so we dont get GET-variables in the result.
        env = self.ENV.copy()
        env['QUERY_STRING'] = ''

        if env.get('REQUEST_METHOD', 'GET') == 'POST':
            _data = FieldStorage(
                fp=self.ENV['wsgi.input'],
                environ=env,
                keep_blank_values=False
            )
            for key in _data.keys():
                value = self._parse_field(_data[key], key, _data)
                if value is not None:
                    self._assign_field_to_section(key, value, data)

        self.POST = data

    def extract_get_data(self):
        "Populates the GET variable from environment"
        ret_dict = {}
        for (key, value) in parse_qsl(self.ENV.get('QUERY_STRING', '')):
            if key in ret_dict:
                if not isinstance(ret_dict[key], list):
                    ret_dict[key] = [ret_dict[key]]
                ret_dict[key].append(value)
            else:
                ret_dict[key] = value
        self.GET = ret_dict

    def _assign_field_to_section(self, key, value, storage):
        if isinstance(value, list):
            for val in value:
                self._assign_field_to_section(key, val, storage)
        else:
            if (isinstance(value, tuple) and value[1] and
              (isinstance(value[1], file) or hasattr(value[1], 'read'))):

                # If an existing value exists for this key, convert to
                # list-result
                if key in self.FILES and \
                  not isinstance(self.FILES[key], list):
                    self.FILES[key] = [self.FILES[key]]

                if key in self.FILES and isinstance(self.FILES[key], list):
                    self.FILES[key].append(value)
                else:
                    self.FILES[key] = value
            elif isinstance(value, basestring):
                # If an existing value exists for this key,
                # convert to list-result
                if key in storage and not isinstance(storage[key], list):
                    storage[key] = [storage[key]]

                if key in storage and isinstance(storage[key], list):
                    storage[key].append(value)
                else:
                    storage[key] = value

    def _parse_field(self, field, key, data):
        value = data.getvalue(key)

        if isinstance(field, list):
            value = [self._parse_field(f, key, data) for f in field]

        elif hasattr(field, 'filename') and field.filename:
            if field.file:
                value = (field.filename, field.file)
            else:
                value = (field.filename, StringIO(data.getvalue(key)))

        elif isinstance(value, basestring):
            try:
                value = unicode(value, 'utf-8')
            except UnicodeDecodeError:
                # If we can't understand the data as utf, try latin1
                value = unicode(value, 'iso-8859-1')

        return value
