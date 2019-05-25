import requests
class Auth:


    def __init__(self,access_code,client_id,client_secret):
        self.access_code = access_code
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        # return token
