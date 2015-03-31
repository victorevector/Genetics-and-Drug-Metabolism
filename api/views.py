from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from Client import _23AndMeClient, SCOPE
import requests
from andMe.settings import CLIENT_ID, CALLBACK_URL
from api.forms import QueryForm
from django import forms

def index(request):
    API_URL = "https://api.23andme.com/authorize"
    params = {  
            "client_id": CLIENT_ID,
            "response_type": 'code',
            "scope": SCOPE,
            "redirect_uri":  CALLBACK_URL, } 
    get_request = requests.Request('GET', url = API_URL, params = params) .prepare()
    context_dict = {
        'auth_url': get_request.url, }
    return render(request, 'api/index.html', context_dict )

def callback(request):
    auth_code = request.GET.get('code')
    if not auth_code:
        raise Http404
    client = _23AndMeClient()
    client.get_token(auth_code)
    # # data['rs2395029']
    request.session['token'] = client.access_token
    return redirect('query_api')

def query_api(request):
    context_dict = {}
    access_token = request.session['token']
    if request.method == 'POST':
        c = _23AndMeClient(access_token)
        user = c.get_names()
        profiles = user['profiles'] #profiles : [ { first_name: ..., last_name: ..., id: ... }, { ..... } ]
        names_and_id = {}
        names = []
        for profile in profiles:
            first_name = profile['first_name']
            names_and_id[first_name] = profile['id']
            name = first_name, first_name
            names.append(name)
        class QueryUserForm(QueryForm):
            profile_name = forms.ChoiceField(choices = names, required = True)
        form = QueryUserForm(request.POST)
        if form.is_valid():
            profile_name = form.cleaned_data['profile_name']
            profile_id = names_and_id[profile_name]
            snp = 'rs2395029' #in future, this will not be hardcoded, but will be a choice for user
            response = c.get_genotype(profile_id = profile_id, locations = snp )
            pairs = response[snp]
            context_dict['carrier_status'] = pairs
            return render(request, 'api/results_api.html', context_dict)
    else:
        c = _23AndMeClient(access_token)   
        user = c.get_names()
        profiles = user['profiles'] #profiles : [ { first_name: ..., last_name: ..., id: ... }, { ..... } ]
        names_and_id = {}
        names = []
        for profile in profiles:
            first_name = profile['first_name']
            names_and_id[first_name] = profile['id']
            name = first_name, first_name
            names.append(name)
        class QueryUserForm(QueryForm):
            profile_name = forms.ChoiceField(choices = names, required = True)
        form = QueryUserForm()
        context_dict['form'] = form
        # context_dict['token'] = token
        return render(request, 'api/query_api.html', context_dict)
