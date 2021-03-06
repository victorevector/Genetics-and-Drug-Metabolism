from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from Client import _23AndMeClient, SCOPE
import requests
from andMe.settings import CLIENT_ID, CALLBACK_URL
from api.forms import QueryForm
from django import forms
from api.models import DrugsAndSNP
from Allele_Interpretation import carrier_status

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
    request.session['token'] = client.access_token
    request.session.set_expiry(0)
    return redirect('query_api')

def query_api(request):
    context_dict = {}
    if 'token' in request.session:
        access_token = request.session['token']
    else:
        return redirect('/api')

    ###Pulls profile name_choices that exist within the same account###
    client = _23AndMeClient(access_token)
    user = client.get_names()
    profiles = user['profiles'] #profiles : [ { first_name: ..., last_name: ..., id: ... }, { ..... } ]
    profile_name_choices = []
    for profile in profiles:
        full_name = profile['first_name'] + ' ' + profile['last_name']
        profile_name_choices.append( (profile['id']+'$'+full_name, full_name) )
    class QueryUserForm(QueryForm):
        profile_name = forms.ChoiceField(choices = profile_name_choices, required = True)

    if request.method == 'POST':
        form = QueryUserForm(request.POST)
        if form.is_valid():
            profile_info = form.cleaned_data['profile_name'].split('$')
            profile_id, profile_name = profile_info[0], profile_info[1]
            drug = form.cleaned_data['drug']
            drug_object = DrugsAndSNP.objects.get(drug = drug)
            snp = drug_object.snp
            api_response = client.get_genotype(profile_id = profile_id, locations = snp )
            users_pairs = api_response[snp]
            context_dict['user_pair'] = users_pairs
            context_dict['nucleic_acid1'] = users_pairs[0]
            context_dict['nucleic_acid2'] = users_pairs[1]
            context_dict['profile_name'] = profile_name
            context_dict['drug_object'] = drug_object
            status = carrier_status(drug=drug,pair=users_pairs)
            context_dict['status'] = status

            return render(request, 'api/results_api.html', context_dict)
    else:
        form = QueryUserForm()
        context_dict['form'] = form
        return render(request, 'api/query_api.html', context_dict)
