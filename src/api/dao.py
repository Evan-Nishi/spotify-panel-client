import requests

def curr_track(access_token):
    #Returns current track as JSON object

    #Params:
    #   access_token(str): access token obtained from ./auth.py

    #Returns:
    #   JSON object: response object with curr track info OR 204 if empty

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    req = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers)

    if req.status_code == 204:
        return 204
    return req