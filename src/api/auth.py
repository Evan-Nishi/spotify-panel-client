from base64 import b64encode
import requests

def get_access_token(ref_token, client_id, client_secret):
    '''
    Returns access token as string 

    Params:
       ref_token(str): refresh token in dotenv
       client_id(str): client id of app
       client_secret(str): client secret of app

    Returns:
        string: new refresh token or error code 
    '''
    print('Fetching access tokens')

    #api requires b64 encoded str <id:secret> format
    cli_bytes = (client_id + ':' + client_secret).encode('ascii')
    cli_header = b64encode(cli_bytes).decode('ascii')
    headers = {'Authorization': 'Basic ' + cli_header}
    form = {
        'grant_type': 'refresh_token',
        'refresh_token': ref_token
    }

    req = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=form, json=True)
    
    print('Status:' + str(req.status_code))

    res = req.json()

    return res['access_token']

#TODO: implement PKCE auth flow for easier setup
'''
def pkce_access_token(state = 0, client_id ):
    #Returns access token when PKCE is enabled

    #Params:
    #   state(string): optional but prevents csrf attacks
    #   client_id(string): client app id
'''