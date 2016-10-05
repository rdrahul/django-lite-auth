class FacebookAuth(object):
    ''' Facebook Oauth Authentication '''
    AUTHORIZATION_URL  ="https://www.facebook.com/v2.7/dialog/oauth"
    
    def get_redirect_url(self, request):
        pass
    def send_code(self, request):
        pass
    def register_user(self, request):
        pass
    def prepare_data(self , response, access_token):
        pass

