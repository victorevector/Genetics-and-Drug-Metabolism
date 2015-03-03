from django.shortcuts import render
from django.shortcuts import redirect
from requests import Request

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
