from django.middleware.csrf import get_token
from django.conf import settings
from django.core.urlresolvers import reverse
import urllib
import requests
import json
from .models import 

class LinkedinAuth(object):
    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    ACCESSTOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
    STATE_TOKEN = None
    
    @staticmethod   
    def get_redirect_url(request):
        """ performs authorization call for linkedin oauth """    

        try:
            #get the redirect url from settings
            redirect_url = request.build_absolute_uri( getattr(settings,'REDIRECT_URL',None) )
            if redirect_url == None:
                raise
            
            #get the client id from settings
            client_id = getattr( settings, 'LINKEDIN_ID',None )
            if client_id == None:
                raise
            
            LinkedinAuth.STATE_TOKEN = get_token(request)
            #GET parameters to be passed
            payload = { 'response_type':'code',
                        'client_id'    : client_id,
                        'redirect_uri' : redirect_url,
                        'state'        : LinkedinAuth.STATE_TOKEN,
                    }
            
            #url
            url = LinkedinAuth.AUTHORIZATION_URL+ '?' + urllib.urlencode(payload)
            return url

        except :
            print ( "Linkedin settings not configured properly" )
    
    @staticmethod
    def send_code( request ):
        code = request.GET.get('code',None)
        state = request.GET.get('state',None)

        if state !=  LinkedinAuth.STATE_TOKEN :
            #some shit went wrong 
            return

        #send request to obtain access token
        #extract below lines away
        client_id = getattr( settings, 'LINKEDIN_ID',None )
        client_secret = getattr( settings, 'LINKEDIN_SECRET',None )
        redirect_url = request.build_absolute_uri( getattr(settings,'REDIRECT_URL',None) )
        

        data = {
            'grant_type'    : 'authorization_code' ,
            'code'          : code ,
            'redirect_uri'  : redirect_url ,
            'client_id'     : client_id , 
            'client_secret' : client_secret ,
        }

        response = requests.post(LinkedinAuth.ACCESSTOKEN_URL , data=data)
        response = json.loads(response.text)
        
        access_token = response['access_token']
        state = response['state']

        print "Access Token " , access_token
        #create a new user or authenticate the previous one
        register_user(access_token)
    
    @static_method
    def register_user(access_token):
        
        

