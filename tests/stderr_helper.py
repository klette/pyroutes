import logging
import sys

import pyroutes

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

real_stderr = sys.stderr
fake_stderr = StringIO.StringIO()
real_loghandlers = pyroutes.logger.handlers
fake_loghandlers = [logging.StreamHandler(fake_stderr)]

logging.basicConfig(level=logging.DEBUG)

def redirect_stderr():
    sys.stderr = fake_stderr
    pyroutes.logger.handlers = fake_loghandlers

def revert_stderr():
    sys.stderr = real_stderr
    pyroutes.logger.handlers = real_loghandlers

def get_stderr_data():
    fake_stderr.seek(0)
    data = fake_stderr.read()
    fake_stderr.truncate(0)
    return data
