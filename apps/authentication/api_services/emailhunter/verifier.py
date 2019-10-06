import requests


class EmailHunterVerifier:
    def __init__(self, api_key, api_version='v2'):
        self.api_key = api_key
        self.api_version = api_version
        self.base_params = {'api_key': api_key}
        self.base_endpoint = 'https://api.hunter.io/{}/'.format(api_version)

    def _make_request(self, endpoint, params):
        res = requests.get(endpoint, params)
        res.raise_for_status()
        data = res.json()

        return data['data']

    def email_verifier(self, email):
        """
        Verify the deliverability of a given email address.abs
        :param email: The email address to check.
        :return: Full payload of the query as a dict.
        """
        params = {'email': email, 'api_key': self.api_key}
        endpoint = self.base_endpoint + 'email-verifier'

        return self._make_request(endpoint, params)
