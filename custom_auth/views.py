from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from auth_backend import AuthenticationManager
from django.http import HttpResponse, HttpResponseRedirect


def login( request , backend ):
    url=AuthenticationManager.perform_authentication(backend, request)
    print (url)
    return HttpResponseRedirect(url)
    
def logout(request):
    return redirect('/')

def home(request):
    return render(request,'index.html' )

def redirect( request ):
    if request.GET.get('error',False):
        print "Error Occured -- do  error recovery callback "
    
    elif request.GET.get('code', False ):
        AuthenticationManager.code_callback(request)
    
    elif request.GET.get('access_token',False):
        AuthenticationManager.access_token_callback(request)
    
    return render(request,'some.html')
    