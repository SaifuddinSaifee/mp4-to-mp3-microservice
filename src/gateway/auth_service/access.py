import os, requests

def login(req):
    auth = req.authorization

    if not auth:
        return None, ("Invalid Credentials", 401)
    
    # If the auth is valid
    basicAuth = (auth.username, auth.password)

    res = requests.post(
        f'http://{os.environ.get("AUTH_SVC_ADDRESS")}/login', # Posts to auth/server.py "login route"
        auth = basicAuth
    )

    # If response from above is 200
    if res.status_code == 200:
        return res.txt, None
    else:
        return None, (res.txt, res.status_code)
        
    
