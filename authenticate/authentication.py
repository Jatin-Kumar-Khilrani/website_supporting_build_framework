import ldap
import logging
import views
from django.contrib.auth.models import User

class auth_user:
    LOGGER = logging.getLogger(__file__)
     
    AD_LDAP_URL = 'ldap://ds.cisco.com:389'
     
    AD_SEARCH_DN = 'OU=Employees,OU=Cisco Users,DC=cisco,DC=com'
     
    AD_SEARCH_FIELDS = dict(
        email      = 'mail',
        first_name = 'givenName',
        last_name  = 'sn',
    )
    def ldap_bind(self,userid,password):
        try:
            active_dir = ldap.initialize(self.AD_LDAP_URL)
            active_dir.simple_bind_s('%s@cisco.com' % userid, password)
            result = active_dir.search_ext_s(self.AD_SEARCH_DN, ldap.SCOPE_SUBTREE,
                   "CN=%s" % userid, self.AD_SEARCH_FIELDS.values())[0][1]
            active_dir.unbind_s()
            for prop, field in self.AD_SEARCH_FIELDS.items():
                value = None
                if field in result:
                    value = result[field][0]
            return True,result
        except ldap.LDAPError, e:
            print e
            return False,{}
#             handle error however you like    