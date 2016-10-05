from .models import OAuthUser

def create_user(data):
    ''' creates the user object '''
    user , created = OAuthUser.objects.get_or_create( data )
    setattr( user , "access_token", data["access_token"] )
    user.save()

