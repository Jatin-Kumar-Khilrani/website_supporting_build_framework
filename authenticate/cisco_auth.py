import urllib2
import urllib
import datetime
import httplib


from xml.etree import ElementTree
import requests 
import ssl

from models import users

import httplib, ssl, urllib2, socket
class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            print("Trying SSLv3.")
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)

class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)



class cisco_auth():



    
    def isvalid(self,user_id,password):

#           opener = urllib2.install_opener(HTTPSHandlerV3())
#           urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))
#           req = urllib2.urlopen('https://sso.cisco.com/autho/forms/CDClogin.html')
#           response = req.read()
#           req.close()
           
           r = requests.get('https://sso.cisco.com/autho/forms/CDClogin.html', auth=('user', 'pass'))
           response = r.text
           return response
    
