from .models import OAuthUser


class AuthBackend(): 
    ''' Custom Authenticaton Backend class for logging users in '''   
    
    def authenticate( self, id=None, access_token = None ):
        try:
            user = OAuthUser.objects.get(user_id = id, access_token = access_token)
            return user
        except:
            return None 

    def get_user(self,user_id):
        try:    
            return OAuthUser.objects.get(pk=user_id)
        except:
            return None


