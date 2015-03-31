# RIght now, the AndMeClient is really an AndMeClient hardcoded for the 23andMe api.
# Wouldnt it be cool to abstract it for general purpose use? And then either create a subclass that appends 23andMe API functionality, or
# Add  23andMe API functionality through a decorator?

import requests
from andMe.settings import CLIENT_ID, CLIENT_SECRET, CALLBACK_URL

GRANT_TYPE = 'authorization_code'
SCOPE = 'basic genomes names'
TOKEN_URL = 'https://api.23andme.com/token/'
BASE_URL = "https://api.23andme.com/1/"


class _23AndMeClient(object):
    # Oauth2 toolkit --23andMe API Client
    def __init__(self, access_token = None):
        self.access_token = access_token

    def get_token(self, auth_code):
        """
        Given an auth_code, this method will retrieve an access token, save the access token to the object  (attribute: self.access_token ) , and return access & refresh token
        """
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': GRANT_TYPE,
            'code': auth_code,
            'redirect_uri': CALLBACK_URL,
            'scope': SCOPE,
        }
        url = TOKEN_URL
        response = requests.post(TOKEN_URL, params) 
        token_data = response.json()
        if 'error' in token_data:
            return token_data['error']
        else:
            self.access_token = token_data['access_token']
            return token_data['access_token'], token_data['refresh_token']

    def refresh_token(self, refresh_token):
        pass 
        # use when auth token expires (1 day)
        # retrieves auth token & refresh token with previously assigned refresh token
        # returns usable auth token & refresh token

    def _get_resource(self, resource):
        # this method gets called by other methods, specifically those that request specific pieces of information from the API
        if self.access_token is None:
            raise Exception('access_token cannot be None')

        headers = {"Authorization": "Bearer {}".format(self.access_token)}
        url = BASE_URL + resource
        response = requests.get(url, headers= headers, verify = False)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_genotype(self,profile_id, locations):
        # calls _get_resource('') and passes the right arguments to get genotype data (json)
        # returns basepairs of the given location(s)
            # e.g. AA, DD, DI, __, --
        # profile_id = "SP1_MOTHER_V4" #I AM USING THE 
        return self._get_resource('demo/genotypes/{}/?locations={}'.format(profile_id, locations) )

    def get_user(self):
        return self._get_resource('demo/user/')

    def get_names(self):
        return self._get_resource('demo/names/')



    