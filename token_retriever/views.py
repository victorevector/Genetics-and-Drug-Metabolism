from django.shortcuts import render
from django.shortcuts import redirect
from requests import Request, post
from django.http import Http404
from django.http import HttpResponse

def index(request):
    return HttpResponse('hi!')

def url_constructor(request):
    API_URL = "https://api.23andme.com/authorize"
    client_id = "ba2a5b529548f7c541a14887f5b54aa9"
    response_type = 'code'
    scope = "names"
    redirect_uri = "http://localhost:8000/token_retriever/callback/"
    params = {  
            "client_id": client_id,
            "response_type": response_type,
            "scope": scope,
            "redirect_uri":  redirect_uri, } 
    get_request = Request('GET', url = API_URL, params = params).prepare()
    return redirect(get_request.url)

def callback(request):
    ##AUTHENTICATION CODE##
    code = request.GET.get('code')
    if not code:
        raise Http404
    #TOKEN##
    params = {
        "client_id": "ba2a5b529548f7c541a14887f5b54aa9",
        "client_secret": "f48c6a139ede44f2b453e112cdda979f",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/token_retriever/callback/",
        "scope": "names",
    }   
    headers = {"accept": "application/json"}
    url = "https://api.23andme.com/token/"
    token_request = post(url, data = params)

    # if not token_request.ok:
    #     raise Http404
    token_data = token_request.json()
    if 'error' in token_data:
        return HttpResponse('TOKEN NOT GIVEN')
    else:
        token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        return HttpResponse( "token: {} ++++ refresh token: {}".format(token,refresh_token) )

