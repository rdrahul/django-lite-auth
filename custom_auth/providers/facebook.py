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


class FacebookAuth(object):
    ''' Facebook Oauth Authentication '''
    AUTHORIZATION_URL  ="https://www.facebook.com/v2.7/dialog/oauth"
    ACCESSTOKEN_URL = "https://graph.facebook.com/v2.7/oauth/access_token"
    PEOPLEINFO_URL = "https://graph.facebook.com/v2.7/me"
    SCOPE = [ 'public_profile', 'email' ]
    DATA_FIELDS  =[
        ('user_id', 'id'),
        ('first_name','first_name'),
        ('last_name', 'last_name'),
        ('email_address' , 'email')
    ]
    STATE_TOKEN = None

    def get_redirect_url(self, request):
        """ performs authorization call for linkedin oauth """    
        try:
            #get the redirect url from settings
            redirect_url = request.build_absolute_uri( getattr(settings,'REDIRECT_URL',None) )
            if redirect_url == None:
                raise
            
            #get the client id from settings
            client_id = getattr( settings, 'FACEBOOK_ID',None )
            if client_id == None:
                raise
            
            #may create a vulnerability change this 
            self.STATE_TOKEN = get_token(request)
            
            #GET parameters to be passed
            payload = { 'response_type':'code',
                        'client_id'    : client_id,
                        'redirect_uri' : redirect_url,
                        'state'        : self.STATE_TOKEN,
                        'scope'        : ','.join(self.SCOPE)
                    }
            
            #create the full url 
            url = self.AUTHORIZATION_URL+ '?' + urlencode(payload,True)
            return url

        except :
            print ( "Facebook settings not configured properly" )
            print (sys.exc_info())

    def send_code(self, request):
        code = request.GET.get('code',None)
        state = request.GET.get('state',None)

        if state !=  self.STATE_TOKEN :
            #some shit went wrong
            print (" Something wrong with the state token") 
            return redirect('/');

        #send request to obtain access token
        #extract below lines away
        client_id = getattr( settings, 'FACEBOOK_ID',None )
        client_secret = getattr( settings, 'FACEBOOK_SECRET',None )
        redirect_url = request.build_absolute_uri( getattr(settings,'REDIRECT_URL',None) )
        

        data = {
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
    
    def register_user(self, access_token):
        ''' Gets the user data from   '''
        fields = [ val[1] for val in self.DATA_FIELDS ]
        fields = ','.join( fields)
        payload = { 'fields' : fields,
                    'access_token':access_token
                     } 

        response = requests.get(  url = self.PEOPLEINFO_URL.format(fields), params = payload)
        print ( response.text )
        data = self.prepare_data( json.loads(response.text) ,access_token )
        return data


    def prepare_data(self , response, access_token):
        ''' Prepare the data for creating a new user '''
        data = {}
        data_fields = self.DATA_FIELDS

        #form a dictionary for creating a user object
        for val in data_fields:
            data [ val[0] ] = response.get(val[1] , None)
        
        data['access_token'] = access_token
        return data

