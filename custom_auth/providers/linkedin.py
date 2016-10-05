#python imports
import requests
import json
import sys
import time
from  urllib.parse import urlencode

#django imports
from django.middleware.csrf import get_token
from django.conf import settings
from django.core.urlresolvers import reverse

#app imports
from custom_auth.models import OAuthUser


class LinkedinAuth(object):
    ''' Performs Linkedin OAuth2 Authentication  '''

    AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
    ACCESSTOKEN_URL   = "https://www.linkedin.com/oauth/v2/accessToken"
    PEOPLEINFO_URL    = "https://api.linkedin.com/v1/people/~:({0})"
    DATA_FIELDS       = [ ('user_id','id') ,
                        ('first_name', 'firstName'),
                        ('last_name','lastName'),
                        ('email_address','emailAddress') ]
    STATE_TOKEN = None
    
    def get_redirect_url(self, request):
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
            
            self.STATE_TOKEN = get_token(request)
            
            #GET parameters to be passed
            payload = { 'response_type':'code',
                        'client_id'    : client_id,
                        'redirect_uri' : redirect_url,
                        'state'        : self.STATE_TOKEN,
                    }
            
            #create the full url 
            url = self.AUTHORIZATION_URL+ '?' + urlencode(payload,True)
            return url

        except :
            print ( "Linkedin settings not configured properly" )
            print (sys.exc_info())
    
    
    def send_code(self, request ):
        code = request.GET.get('code',None)
        state = request.GET.get('state',None)

        if state !=  self.STATE_TOKEN :
            #some shit went wrong
            print (" Something wrong with the state token") 
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

        response = requests.post(self.ACCESSTOKEN_URL , data=data)
        response = json.loads(response.text)
        print (response)
        access_token = response.get('access_token',None)
        state = response.get('state',None)

        print ("Access Token " , access_token )
        #create a new user or authenticate the previous one
        return self.register_user(access_token)
    

    def register_user(self,access_token):
        #checks if user exist

        # gets a user data
        headers = { 'Authorization' : 'Bearer ' + access_token,
                    'Content-Type': 'application/json',
                    'x-li-format':'json' }

        payload = {'format' : 'json' }
        
        fields = ['first_name','id','emailAddress','last_name']
        fields = ','.join ( fields )
        
        response =  requests.get(  url = self.PEOPLEINFO_URL.format(fields), params = payload, headers = headers );
        print ( response.text )
        data = self.prepare_data( json.loads(response.text) ,access_token )
        return data
    
    def prepare_data(self, response, access_token):
        ''' Prepare the data for creating a new user '''
        data = {}
        data_fields = self.DATA_FIELDS

        #form a dictionary for creating a user object
        for val in data_fields:
            data [ val[0] ] = response.get(val[1] , None)
        
        data['access_token'] = access_token
        return data