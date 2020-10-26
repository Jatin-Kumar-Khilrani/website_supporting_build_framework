from django.contrib.auth.models import User
import ldap
import logging
 
from user_profiles.models import UserProfile
 
LOGGER = logging.getLogger(__file__)
 
AD_LDAP_URL = 'ldap://ds.cisco.com:389'
 
AD_SEARCH_DN = 'OU=Employees,OU=Cisco Users,DC=cisco,DC=com'
 
AD_SEARCH_FIELDS = dict(
    email      = 'mail',
    first_name = 'givenName',
    last_name  = 'sn',
)
 
class ActiveDirectoryBackend(object):
 
    def authenticate(self, username=None, password=None):
        # Disallowing null or blank string as password
        if password is None or password == '':
            return None
 
        try:
            active_dir = ldap.initialize(AD_LDAP_URL)
            active_dir.simple_bind_s('%s@cisco.com' % username, password)
            result = active_dir.search_ext_s(AD_SEARCH_DN, ldap.SCOPE_SUBTREE,
                   "CN=%s" % username, AD_SEARCH_FIELDS.values())[0][1]
            active_dir.unbind_s()
 
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff     = False
                user.is_superuser = False
            finally:
 
                # Make sure all users have a profile, if not create one.
                try:
                    user.get_profile()
                except UserProfile.DoesNotExist:
                    try:
                        UserProfile.objects.create(user_id=user.id)
                        LOGGER.info('Created user profile for %s' % username)
                    except:
                        LOGGER.exception('Failed to create user profile for %s'
                            % username)
 
                for prop, field in AD_SEARCH_FIELDS.items():
                    value = None
                    if field in result:
                        value = result[field][0]
                    setattr(user, prop, value)
                user.save()
 
            return user
        except ldap.LDAPError:
            return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

if __name__ == "__main__":
    obj = ActiveDirectoryBackend()
    obj.authenticate('sausuvar','')
    