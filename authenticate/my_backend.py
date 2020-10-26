from models import users
from cisco_auth import cisco_auth

class MyBackend:
    def authenticate(self, userid=None, password=None):
        try:
            return users.objects.get(email=userid+'@cisco.com')
        except users.DoesNotExist:
            return None 
                
    def get_user(self, userid):
        try:
            return users.objects.get(pk=userid)
        except users.DoesNotExist:
            return None