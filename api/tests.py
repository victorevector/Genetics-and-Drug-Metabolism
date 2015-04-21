# Can the my app generate a token by successfully implementing oauth2 protocal?
# Can the app make calls to the 23andMe API?
# Can the app receive responses from the API?

from django.test import TestCase
import responses
import requests
import json
import  Client

class ClientTestCase(TestCase):
    @responses.activate
    def test_get_token_with_valid_auth_code_as_method_argument(self):
        client = Client._23AndMeClient()
        valid_auth_code = '1928789'
        expected_access_token = "89822b93d2"
        json_response = '{"access_token": "%s", "token_type":"bearer","expires_in": 86400,"refresh_token":"33c53cd7bb","scope": "%s" }' % (expected_access_token, Client.SCOPE)
        responses.add( responses.POST,
            Client.TOKEN_URL,
            body = json_response,
            status = 200,
            content_type = 'application/json'
            )

        self.assertEqual(client.get_token(valid_auth_code)[0], expected_access_token)
        self.assertEqual(client.access_token, expected_access_token)

    @responses.activate
    def test_get_token_with_invalid_auth_code_as_method_argument(self):
        client = Client._23AndMeClient()
        invalid_auth_code = '123456789'
        expected_access_token = 'invalid_request'
        json_response = '{"error_description":"No such code: %s","error":"invalid_request"}' % (invalid_auth_code)
        responses.add( responses.POST,
            Client.TOKEN_URL,
            body = json_response,
            content_type ='application/json'
            )

        self.assertEqual(client.get_token(invalid_auth_code), 'invalid_request')

    def test_refresh_token(self):
        pass

    @responses.activate
    def test_get_resources_ability_to_handle_valid_requests_to_api(self):
        json_response = '{"id": "a42e94634e3f7683", "profiles": [{ "genotyped": true, "id": "c4480ba411939067"} ] }'
        url = Client.BASE_URL + 'user'
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type = 'application/json',
            status = 200 
            )
        client = Client._23AndMeClient('89822b93d2')
        expected_json_response = json.loads(json_response)

        self.assertEqual(client._get_resource('user'), expected_json_response)

    @responses.activate
    def test_get_resources_ability_to_handle_invalid_request_to_api(self):
        json_response = '{ "error": "invalid_request", "error_description": "error_description" }'
        url = Client.BASE_URL + 'user'
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type = 'application/json',
            status = 400
            )
        client = Client._23AndMeClient('89822b93d2')

        self.assertRaises(requests.exceptions.HTTPError, client._get_resource, 'user')

    @responses.activate
    def test_get_genotype_with_valid_profile_id_and_valid_locations_as_method_arguments(self):
        json_response = '{ "i3000001": "II", "rs3094315": "AA", "id": "c4480ba411939067"}'
        profile_id = "c4480ba411939067"
        locations = "rs3094315"
        url = "https://api.23andme.com/1/demo/genotypes/{}/?locations={}".format(profile_id, locations) 
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type ='application/json',
            status = 200,
            match_querystring=True
            )
        client = Client._23AndMeClient('89822b93d2')
        expected_json_response = json.loads(json_response)
        self.assertEqual(client.get_genotype(profile_id= profile_id, locations=locations), expected_json_response )

    @responses.activate
    def test_get_genotypes_ability_to_handle_valid_requests_to_api(self):
        json_response = '{ "i3000001": "II", "rs3094315": "AA", "id": "c4480ba411939067"}'
        profile_id = "c4480ba411939067"
        locations = "rs3094315"
        url = "https://api.23andme.com/1/demo/genotypes/{}/?locations={}".format(profile_id, locations) 
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type ='application/json',
            status = 200,
            match_querystring=True
            )
        client = Client._23AndMeClient('89822b93d2')
        expected_json_response = json.loads(json_response)
        self.assertEqual(client.get_genotype(profile_id= profile_id, locations=locations), expected_json_response )

    @responses.activate
    def test_get_genotypes_ability_to_handle_invalid_request_to_api(self):
        json_response = '{ "error": "invalid_request", "error_description": "error_description" }'
        profile_id = "invalid_profile_id"
        locations = "invalid_location"
        url = "https://api.23andme.com/1/demo/genotypes/{}/?locations={}".format(profile_id, locations) 
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type = 'application/json',
            status = 400,
            match_querystring=True
            )
        client = Client._23AndMeClient('89822b93d2')

        self.assertRaises(requests.exceptions.HTTPError, client.get_genotype, profile_id, locations)

    @responses.activate
    def test_get_users_ability_to_handle_valid_requests_to_api(self):
        json_response = '{ "id": "a42e94634e3f7683", "profiles": [ { "genotyped": true, "id": "c4480ba411939067"} ] }'
        url = Client.BASE_URL + 'demo/user/'
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type ='application/json',
            status = 200
            )
        client = Client._23AndMeClient('89822b93d2')
        expected_json_response = json.loads(json_response)

        self.assertEqual(client.get_user(), expected_json_response) 

    @responses.activate
    def test_get_users_ability_to_handle_invalid_request_to_api(self):
        json_response = '{ "error": "invalid_request", "error_description": "error_description" }'
        url = Client.BASE_URL + 'demo/user/' 
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type = 'application/json',
            status = 400
            )
        client = Client._23AndMeClient('89822b93d2')

        self.assertRaises(requests.exceptions.HTTPError, client.get_user)

    @responses.activate
    def test_get_names_ability_to_handle_valid_requests_to_api(self):
        json_response = '{"first_name": "Gregor", "last_name": "Mendel", "id": "a42e94634e3f7683", "profiles": [ { "first_name": "Johann", "last_name": "Mendel", "id": "c4480ba411939067"} ] }'
        url = Client.BASE_URL + 'demo/names/'
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type ='application/json',
            status = 200
            )
        client = Client._23AndMeClient('89822b93d2')
        expected_json_response = json.loads(json_response)

        self.assertEqual(client.get_names(), expected_json_response) 

    @responses.activate
    def test_get_names_ability_to_handle_invalid_request_to_api(self):
        json_response = '{ "error": "invalid_request", "error_description": "error_description" }'
        url = Client.BASE_URL + 'demo/names/' 
        responses.add(responses.GET,
            url,
            body = json_response,
            content_type = 'application/json',
            status = 400
            )
        client = Client._23AndMeClient('89822b93d2')

        self.assertRaises(requests.exceptions.HTTPError, client.get_names)

class ViewsTestCase(TestCase):
    pass
    def setup(self):
        pass


