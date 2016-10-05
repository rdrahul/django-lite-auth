from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . import providers
from .providers.linkedin import LinkedinAuth
from .providers.facebook import FacebookAuth

from .utility import create_user

from django.contrib.auth import authenticate , login
class AuthenticationManager(object):
    current_backend=None
    providers = ['LinkedinAuth' , 'FacebookAuth']
    @staticmethod
    def perform_authentication( auth_provider, request ):
        """ performs authentication for a given provider """
        
        provider = auth_provider.capitalize() + 'Auth'
        if provider not in AuthenticationManager.providers :  
            return redirect('/')
        
        AuthenticationManager.current_backend  = eval(provider)()
        return AuthenticationManager.current_backend.get_redirect_url(request)
   
    @staticmethod
    def code_callback( request ):
        """ wrapper for sending code to provider """ 
        print ('current_backend ',AuthenticationManager.current_backend)
        provider = AuthenticationManager.current_backend
        if provider != None:
            print (" => " ,provider)
            data = provider.send_code(request)
            print (data)
            if data != None:
                create_user(data)
                print("here")
                user = authenticate( id =data["user_id"], access_token = data["access_token"] )
                login(request,user )
                
