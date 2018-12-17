import requests
import logging
import robot
import urllib
import urllib3
import os
from robot.api import logger
from robot import utils
from robot.libraries.BuiltIn import BuiltIn
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault


class ZeepKeywords:

    def __init__(self):
        self._cache = robot.utils.ConnectionCache('No sessions created')
        self.builtin = BuiltIn()


    def create_soap_client(
                    self,
                    url_or_path,
                    alias=None,
                    cookies=None,
                    auth=None,
                    timeout='90 seconds',
                    proxies=None,
                    verify=False,
                    debug=0,
                    disable_warnings=1):
        
        
        self.builtin.log('Creating session: %s' % url_or_path, 'DEBUG')
        s = session = requests.Session()

        auth = requests.auth.HTTPBasicAuth(*auth) if auth else None

        s.auth = auth if auth else s.auth
        s.proxies = proxies if proxies else s.proxies

        if disable_warnings:
            # you need to initialize logging, otherwise you will not see anything from requests
            logging.basicConfig()
            logging.getLogger().setLevel(logging.ERROR)
            zeep_log = logging.getLogger("zeep")
            zeep_log.setLevel(logging.ERROR)
            zeep_log.propagate = True
            if not verify:
                urllib3.disable_warnings(
                    urllib3.exceptions.InsecureRequestWarning)

        # verify can be a Boolean or a String
        if isinstance(verify, bool):
            s.verify = verify
        elif isinstance(verify, str):
            if verify.lower() == 'true' or verify.lower() == 'false':
                s.verify = self.builtin.convert_to_boolean(verify)
            else:
                # String for CA_BUNDLE, not a Boolean String
                s.verify = verify
        else:
            # not a Boolean nor a String
            s.verify = verify

        # self.url = self._get_url(url_or_path)
        self.url = url_or_path

        self._client = Client(self.url, transport=Transport(session=session))
        index = self._cache.register(self._client, alias=alias)
        return index


    def switch_soap_client(self, index_or_alias):
        self._cache.switch(index_or_alias)


    def call_soap_method(self, name, *args):
        """Calls the SOAP method with the given `name` and `args`.

        Returns a Python object graph or SOAP envelope as a XML string
        depending on the client options.
        """

        return self._call(None, None, False, name, *args)

    def _call(self, service, port, expect_fault, name, *args):
        client = self._client
        method = getattr(client.service, name)
        received = None
        try:
            received = method(*args)
            if expect_fault:
                raise AssertionError('The server did not raise a fault.')
        except Fault as e:
            if not expect_fault:
                raise e
            received = str(e)
        return received

    def _get_url(self, url_or_path):
        if not len(urllib.parse.urlparse(url_or_path).scheme) > 1:
            if not os.path.isfile(url_or_path):
                raise IOError("File '%s' not found." % url_or_path)
            url_or_path = 'file:' + urllib.request.pathname2url(url_or_path)
        return url_or_path



# assumed that no WSDL will have a service or port named "1", etc.
def parse_index(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


def to_bool(item):
    if isinstance(item, str):
        if utils.eq(item, 'True'):
            return True
        if utils.eq(item, 'False'):
            return False
    return bool(item)


def format_robot_time(timestr):
    secs = utils.timestr_to_secs(timestr)
    return utils.secs_to_timestr(secs)
