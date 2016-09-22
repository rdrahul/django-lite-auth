from django.shortcuts import redirect
from .providers import linkedin

from .providers.linkedin import LinkedinAuth

class AuthenticationManager(object):
    current_backend=None

    @staticmethod
    def perform_authentication( auth_provider, request ):
        """ performs authentication for a given provider """
        
        provider = getattr(linkedin, auth_provider.capitalize() + 'Auth', None)
        if provider == None:
            return redirect('/')
        
        AuthenticationManager.current_backend  = provider
        return provider.get_redirect_url(request)
   
    @staticmethod
    def code_callback( request ):
        """ wrapper for sending code to provider """ 
        provider = AuthenticationManager.current_backend
        print (" => " ,provider)
        provider.send_code(request)

    @staticmethod
    def access_token_callback(request):
        """ wrapper for getting access token from request """
        provider = AuthenticationManager.current_backend
        provider.get_access_token(request)    
